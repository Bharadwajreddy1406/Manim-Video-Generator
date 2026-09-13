"""Reusable and configurable speech services for narrated Manim scenes."""

import importlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any

from edge_tts import Communicate
from manim_voiceover._typing import VoiceoverData
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import PathLike, SpeechService, path_to_string


class EdgeTtsSpeechService(SpeechService):
    """Generate narration with Microsoft Edge's online neural voices."""

    def __init__(
        self,
        voice: str = "en-IN-NeerjaNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs: object,
    ) -> VoiceoverData:
        cache_dir = self.cache_dir if cache_dir is None else cache_dir
        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "edge-tts",
            "voice": self.voice,
            "rate": self.rate,
            "volume": self.volume,
            "pitch": self.pitch,
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = str(Path(path_to_string(path)).with_suffix(".mp3"))

        output_path = (Path(cache_dir) / audio_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        Communicate(
            input_text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch,
        ).save_sync(str(output_path))

        return {
            "input_text": input_text,
            "input_data": input_data,
            "original_audio": audio_path,
        }


EXTERNAL_SERVICES = {
    "gtts": ("manim_voiceover.services.gtts", "GTTSService", "lang", "gtts"),
    "azure": (
        "manim_voiceover.services.azure",
        "AzureService",
        "voice",
        "azure.cognitiveservices.speech",
    ),
    "elevenlabs": (
        "manim_voiceover.services.elevenlabs",
        "ElevenLabsService",
        "voice_name",
        "elevenlabs",
    ),
    "openai": (
        "manim_voiceover.services.openai",
        "OpenAIService",
        "voice",
        "openai",
    ),
}


def load_voiceover_config(config_path: Path | None) -> dict[str, Any]:
    if config_path is None or not config_path.is_file():
        return {}
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise TypeError(f"Voiceover config must contain a JSON object: {config_path}")
    return config


def create_speech_service(config_path: Path | None = None) -> SpeechService:
    """Create the configured Edge TTS or external speech service."""
    config = load_voiceover_config(config_path)
    service_name = os.getenv(
        "MANIMA_VOICE_SERVICE", str(config.get("service", "edge-tts"))
    ).casefold()
    configured_voice = config.get("voice")
    voice = os.getenv(
        "MANIMA_VOICE",
        configured_voice if isinstance(configured_voice, str) else "",
    )
    configured_options = config.get("options", {})
    if not isinstance(configured_options, dict):
        raise TypeError("voiceover.json 'options' must be a JSON object")
    options = dict(configured_options)

    if service_name in {"edge-tts", "edge"}:
        return EdgeTtsSpeechService(
            voice=voice or "en-IN-NeerjaNeural",
            **options,
        )

    try:
        module_name, class_name, voice_option, requirement = EXTERNAL_SERVICES[
            service_name
        ]
    except KeyError as error:
        supported = ", ".join(["edge-tts", *EXTERNAL_SERVICES])
        raise ValueError(
            f"Unknown voice service {service_name!r}. Supported: {supported}"
        ) from error

    if voice:
        options[voice_option] = voice
    try:
        if importlib.util.find_spec(requirement) is None:
            raise ImportError(requirement)
        module = importlib.import_module(module_name)
        service_class = getattr(module, class_name)
        return service_class(**options)
    except ImportError as error:
        raise RuntimeError(
            f"The {service_name!r} voice provider is not installed. Run "
            f'`uv add "manim-voiceover[{service_name}]"`.'
        ) from error
