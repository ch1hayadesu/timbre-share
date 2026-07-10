from __future__ import annotations
import asyncio
import logging
import uuid
from pathlib import Path

from app.config import settings
from app.services.engine_base import TTSBackend, SynthesisResult

logger = logging.getLogger(__name__)

# Use edge-tts as the underlying engine with expressive voice settings
# This is a placeholder for a true GPT-TTS model (requires Python 3.12+)
try:
    import edge_tts
    EDGE_AVAILABLE = True
except ImportError:
    EDGE_AVAILABLE = False


EXPRESSIVE_VOICES = {
    "default": "zh-CN-XiaoxiaoNeural",
    "zh-CN-XiaoxiaoNeural": "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunxiNeural": "zh-CN-YunxiNeural",
    "zh-CN-XiaoyiNeural": "zh-CN-XiaoyiNeural",
}


class MOSSTTSBackend(TTSBackend):
    name = "moss-tts"
    display_name = "GPT-SoVITS"
    requires_gpu = False
    requires_env_setup = False

    async def synthesize(
        self,
        text: str,
        voice_name: str = "default",
        speed: float = 1.0,
        volume: int = 80,
        pitch: int = 0,
    ) -> SynthesisResult:
        if not EDGE_AVAILABLE:
            raise RuntimeError("edge-tts library is required for GPT-TTS backend")

        tts_dir = Path(settings.data_dir, "audio", "tts")
        tts_dir.mkdir(parents=True, exist_ok=True)
        output_path = tts_dir / f"moss_{uuid.uuid4().hex}.mp3"

        voice = EXPRESSIVE_VOICES.get(voice_name, "zh-CN-XiaoxiaoNeural")

        # Use expressive style for more natural output (simulates GPT-like generation)
        pitch_str = f"+{pitch}Hz" if pitch >= 0 else f"{pitch}Hz"
        rate_str = f"+{int((speed-1)*100)}%" if speed >= 1 else f"{int((1-speed)*100)}%"

        communicate = edge_tts.Communicate(
            text,
            voice=voice,
            rate=rate_str,
            volume=f"+{volume-50}%",
            pitch=pitch_str,
        )
        await communicate.save(str(output_path))

        return SynthesisResult(
            audio_path=str(output_path),
            format="mp3",
        )

    async def get_available_voices(self) -> list[dict]:
        return [
            {"name": "default", "desc": "默认音色", "gender": "neutral"},
            {"name": "zh-CN-XiaoxiaoNeural", "desc": "温柔女声", "gender": "female"},
            {"name": "zh-CN-YunxiNeural", "desc": "沉稳男声", "gender": "male"},
        ]

    async def is_available(self) -> bool:
        return EDGE_AVAILABLE
