from __future__ import annotations
import asyncio
from pathlib import Path

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.repositories.tts_repo import TtsRepo
from app.services import tts_engine

VOICE_MAP = {
    1: "zh-CN-XiaoxiaoNeural",
    2: "zh-CN-YunxiNeural",
    3: "zh-CN-XiaoyiNeural",
    4: "zh-CN-YunjianNeural",
    5: "zh-CN-XiaohanNeural",
}


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def synthesize_tts(self, record_id: int, text: str, voice_id: int,
                   speed: float, volume: int, pitch: int,
                   tts_model: str = "edge-tts"):
    db = SessionLocal()
    try:
        tts_repo = TtsRepo(db)
        record = tts_repo.get_by_id(record_id)
        if not record:
            return {"error": "record not found"}

        tts_repo.update_status(record_id, 2)
        db.commit()

        voice_name = VOICE_MAP.get(voice_id, "zh-CN-XiaoxiaoNeural")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            tts_engine.synthesize(
                text=text,
                voice_name=voice_name,
                speed=speed,
                volume=volume,
                pitch=pitch,
                model=tts_model,
            )
        )
        loop.close()

        audio_dir = Path(settings.data_dir, "audio")
        rel_path = Path(result.audio_path).relative_to(audio_dir).as_posix()
        tts_repo.update_audio(record_id, rel_path)
        return {"record_id": record_id, "audio_path": rel_path}

    except Exception as exc:
        db.rollback()
        try:
            tts_repo = TtsRepo(db)
            tts_repo.update_status(record_id, -1, str(exc))
            db.commit()
        except Exception:
            db.rollback()
        raise self.retry(exc=exc)

    finally:
        db.close()
