from app.services.engine_registry import get_backend, list_available_backends
from app.services.engine_base import SynthesisResult


class TtsEngine:
    MODEL_NAME = "engine-registry"

    async def synthesize(self, text: str, voice_name: str = "zh-CN-XiaoxiaoNeural",
                         speed: float = 1.0, volume: int = 80, pitch: int = 0,
                         engine: str | None = None) -> str:
        backend = get_backend(engine)
        result = await backend.synthesize(text, voice_name, speed, volume, pitch)
        return result.audio_path

    async def get_available_voices(self) -> list[dict]:
        backend = get_backend()
        return await backend.get_available_voices()

    def list_engines(self) -> list[dict]:
        return list_available_backends()


engine = TtsEngine()
