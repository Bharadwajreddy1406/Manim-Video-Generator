# Manima

Manima is a workspace for building mathematical and technical explainer videos
with Manim Community Edition. Each video has its own numbered folder containing
the narration script, visual storyboard, Manim scene, and local assets.

## Repository workflow

New or substantially revised videos follow this sequence:

1. Write and approve `script.md`.
2. Write and approve `storyboard.md`.
3. Implement `scene.py`.
4. Render and review a low-quality preview.
5. Refine timing and layout before producing a higher-quality render.

Reusable visual helpers belong in `shared/`. Video-specific assets belong in
that video's `assets/` folder.

## Project utilities

Run these commands from the repository root on Windows.

```powershell
# Create the next numbered project from videos/_template.
.\create "System Design 01"
# -> videos/002_system_design_01

# Omit the name to generate an auto_XXXXXX suffix.
.\create
# -> videos/003_auto_482901

# Render by number or by the complete project folder name.
.\render 002
.\render 002_system_design_01
```

`render` defaults to Manim's low-quality development preset and writes to the
repository's `media/` directory. It renders every Manim `Scene` declared in the
selected project's `scene.py`. Select another quality when needed:

```powershell
.\render 002 --quality medium
.\render 002 --quality high
.\render 002 --quality 4k
.\render 002 --preview
```

The same utilities can be invoked directly with
`uv run python scripts/create.py` and `uv run python scripts/render.py`.
Command Prompt also accepts the shorter bare forms `create` and `render` from
the repository root.

## Manim Voiceover guide

Narrated videos use `manim-voiceover` so narration timing controls animation
timing. Read [the full Manim Voiceover guide](docs/manim_voiceover.md) before
implementing or changing a narrated scene.

The key repository rules are:

- `script.md` remains the source of truth for spoken narration.
- Use `VoiceoverScene` and divide narration into storyboard-aligned voiceover
  blocks instead of guessing timing with arbitrary waits.
- Use `tracker.duration` and occasional bookmarks to synchronize meaningful
  visual actions with speech.
- Keep speech services replaceable and keep API credentials out of scene files.
- Render voiceover scenes with Manim caching disabled. The `render` utility
  detects direct `manim_voiceover` imports and adds `--disable_caching`
  automatically.
- Re-render and review the complete video with audio whenever the speech service
  or narration changes.
