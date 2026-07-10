from __future__ import annotations
import asyncio
import uuid
from pathlib import Path
from typing import Optional

from app.config import settings
from app.services.engine_registry import (
    get_backend,
    list_available_backends,
    initialize_backends,
)
from app.services.engine_base import SynthesisResult


_backends_initialized = False


def ensure_initialized():
    global _backends_initialized
    if not _backends_initialized:
        initialize_backends()
        _backends_initialized = True


async def synthesize(
    text: str,
    voice_name: str = "zh-CN-XiaoxiaoNeural",
    speed: float = 1.0,
    volume: int = 80,
    pitch: int = 0,
    model: str | None = None,
) -> SynthesisResult:
    ensure_initialized()
    backend = get_backend(model)
    return await backend.synthesize(
        text=text,
        voice_name=voice_name,
        speed=speed,
        volume=volume,
        pitch=pitch,
    )


async def get_available_voices(model: str | None = None) -> list[dict]:
    ensure_initialized()
    backend = get_backend(model)
    return await backend.get_available_voices()


def get_available_models() -> list[dict]:
    ensure_initialized()
    return list_available_backends()


engine = object()

__all__ = [
    "synthesize",
    "get_available_voices",
    "get_available_models",
    "engine",
]
