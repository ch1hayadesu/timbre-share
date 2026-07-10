from __future__ import annotations
import asyncio
import uuid
from pathlib import Path

from app.config import settings
from app.services.engine_base import TTSBackend, SynthesisResult


class EdgeTTSBackend(TTSBackend):
    name = "edge-tts"
    display_name = "Edge TTS（微软云）"
    requires_gpu = False
    requires_env_setup = False

    def __init__(self):
        self._initialized = False

    async def initialize(self):
        if self._initialized:
            return
        try:
            import edge_tts
            self._check = edge_tts
            self._initialized = True
        except ImportError:
            self._initialized = False

    async def synthesize(
        self,
        text: str,
        voice_name: str = "zh-CN-XiaoxiaoNeural",
        speed: float = 1.0,
        volume: int = 80,
        pitch: int = 0,
    ) -> SynthesisResult:
        await self.initialize()

        rate = f"+{int((speed - 1.0) * 100)}%" if speed >= 1.0 else f"-{int((1.0 - speed) * 100)}%"
        vol = f"+{volume - 50}%" if volume >= 50 else f"-{50 - volume}%"
        pitch_str = f"+{pitch}Hz" if pitch >= 0 else f"{pitch}Hz"

        tts_dir = Path(settings.data_dir, "audio", "tts")
        tts_dir.mkdir(parents=True, exist_ok=True)
        output_path = tts_dir / f"{uuid.uuid4().hex}.mp3"

        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice=voice_name, rate=rate, volume=vol, pitch=pitch_str)
            await communicate.save(str(output_path))
        except Exception as e:
            raise RuntimeError(f"TTS synthesis failed: {e}")

        return SynthesisResult(audio_path=str(output_path), format="mp3")

    async def get_available_voices(self) -> list[dict]:
        await self.initialize()
        try:
            import edge_tts
            voices = await edge_tts.list_voices()
            return [
                {"name": v["ShortName"], "locale": v["Locale"], "gender": v["Gender"]}
                for v in voices if v["Locale"].startswith("zh")
            ]
        except Exception:
            return []

    async def is_available(self) -> bool:
        try:
            import edge_tts
            return True
        except ImportError:
            return False
