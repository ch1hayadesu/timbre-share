from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class SynthesisResult:
    audio_path: str
    duration_seconds: float = 0.0
    format: str = "mp3"


class TTSBackend(ABC):
    name: str = ""
    display_name: str = ""
    requires_gpu: bool = False
    requires_env_setup: bool = False

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice_name: str = "zh-CN-XiaoxiaoNeural",
        speed: float = 1.0,
        volume: int = 80,
        pitch: int = 0,
    ) -> SynthesisResult:
        ...

    @abstractmethod
    async def get_available_voices(self) -> list[dict]:
        ...

    async def initialize(self):
        pass

    async def is_available(self) -> bool:
        return True
