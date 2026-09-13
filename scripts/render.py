"""Resolve a numbered video project and render its declared Manim scenes."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

from manim import Scene

if __package__:
    from .create import numbered_projects, repository_root
else:
    from create import numbered_projects, repository_root


QUALITY_FLAGS = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "4k": "-qk",
}


def resolve_project(identifier: str, videos_dir: Path) -> Path:
    projects = numbered_projects(videos_dir)

    if identifier.isdigit():
        requested_number = int(identifier)
        matches = [path for number, path in projects if number == requested_number]
    else:
        matches = [
            path
            for _, path in projects
            if path.name.casefold() == identifier.casefold()
        ]

    if not matches:
        raise FileNotFoundError(
            f"No video project matches {identifier!r} in {videos_dir}"
        )
    if len(matches) > 1:
        names = ", ".join(sorted(path.name for path in matches))
        raise ValueError(f"Project identifier {identifier!r} is ambiguous: {names}")
    return matches[0]


def load_scene_module(scene_file: Path) -> ModuleType:
    module_name = f"_manima_scene_{scene_file.parent.name}"
    spec = importlib.util.spec_from_file_location(module_name, scene_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load scene module: {scene_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declared_scene_names(scene_file: Path) -> list[str]:
    module = load_scene_module(scene_file)
    scenes: list[str] = []
    for name, value in vars(module).items():
        if (
            isinstance(value, type)
            and issubclass(value, Scene)
            and value is not Scene
            and value.__module__ == module.__name__
        ):
            scenes.append(name)
    return scenes


def source_uses_manim_voiceover(source: str, filename: str = "<scene>") -> bool:
    """Return whether source code directly imports Manim Voiceover."""
    tree = ast.parse(source, filename=filename)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(
                alias.name == "manim_voiceover"
                or alias.name.startswith("manim_voiceover.")
                for alias in node.names
            ):
                return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and (
                node.module == "manim_voiceover"
                or node.module.startswith("manim_voiceover.")
            ):
                return True
    return False


def uses_manim_voiceover(scene_file: Path) -> bool:
    return source_uses_manim_voiceover(
        scene_file.read_text(encoding="utf-8"),
        filename=str(scene_file),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="render",
        description=("Render every Manim Scene declared by a numbered video project."),
    )
    parser.add_argument(
        "project",
        help="A numeric prefix such as 034, or a full folder name.",
    )
    parser.add_argument(
        "--quality",
        choices=QUALITY_FLAGS,
        default="low",
        help="Render quality (default: low).",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Open the rendered video after Manim finishes.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repository_root()

    try:
        project_dir = resolve_project(args.project, root / "videos")
        scene_file = project_dir / "scene.py"
        if not scene_file.is_file():
            raise FileNotFoundError(f"Scene file not found: {scene_file}")
        scene_names = declared_scene_names(scene_file)
        if not scene_names:
            raise ValueError(f"No Manim Scene subclasses found in {scene_file}")
        voiceover_enabled = uses_manim_voiceover(scene_file)
    except (FileNotFoundError, ImportError, OSError, ValueError) as error:
        print(f"render: error: {error}")
        return 1

    command = [
        sys.executable,
        "-m",
        "manim",
        QUALITY_FLAGS[args.quality],
    ]
    if args.preview:
        command.append("--preview")
    if voiceover_enabled:
        command.append("--disable_caching")
    command.extend([str(scene_file), *scene_names])

    print(f"Project: {project_dir.name}")
    print(f"Scenes: {', '.join(scene_names)}")
    if voiceover_enabled:
        print("Voiceover: detected (Manim caching disabled)")
    print(f"Output: {root / 'media'}")
    return subprocess.run(command, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
