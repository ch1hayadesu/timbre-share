import asyncio
from pathlib import Path

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.repositories.tts_repo import TtsRepo
from app.repositories.voice_repo import VoiceRepo
from app.services.tts_engine import engine

VOICE_MAP = {
    1: "zh-CN-XiaoxiaoNeural",
    2: "zh-CN-YunxiNeural",
    3: "zh-CN-XiaoyiNeural",
    4: "zh-CN-YunjianNeural",
    5: "zh-CN-YunxiaNeural",
    6: "zh-CN-YunyangNeural",
    7: "zh-CN-liaoning-XiaobeiNeural",
}


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def synthesize_tts(self, record_id: int, text: str, voice_id: int,
                   speed: float, volume: int, pitch: int, engine: str | None = None):
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
        abs_path = loop.run_until_complete(
            engine.synthesize(text, voice_name, speed, volume, pitch, engine=engine)
        )
        loop.close()

        audio_dir = Path(settings.data_dir, "audio")
        rel_path = Path(abs_path).relative_to(audio_dir).as_posix()
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
