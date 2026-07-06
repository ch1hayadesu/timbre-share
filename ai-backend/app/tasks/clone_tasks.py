import os
import subprocess
from pathlib import Path

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.repositories.voice_repo import VoiceRepo


@celery_app.task(bind=True, max_retries=1, default_retry_delay=10)
def process_clone_task(self, voice_id: int, audio_path: str, clone_mode: int):
    db = SessionLocal()
    try:
        voice_repo = VoiceRepo(db)
        voice = voice_repo.get_by_id(voice_id)
        if not voice:
            return {"error": "voice not found"}

        voice_repo.update_status(voice_id, 2)
        db.commit()

        models_dir = Path(settings.data_dir, "models")
        models_dir.mkdir(parents=True, exist_ok=True)

        output_dir = models_dir / f"voice_{voice_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        if clone_mode == 0:
            self._instant_clone(audio_path, output_dir)
        else:
            self._deep_clone(audio_path, output_dir)

        voice_repo.update_status(voice_id, 1)
        db.commit()

        return {"voice_id": voice_id, "model_path": str(output_dir)}

    except Exception as exc:
        db.rollback()
        try:
            voice_repo = VoiceRepo(db)
            voice_repo.update_status(voice_id, -1, str(exc))
            db.commit()
        except Exception:
            db.rollback()
        raise self.retry(exc=exc)

    finally:
        db.close()

    @staticmethod
    def _instant_clone(audio_path: str, output_dir: Path):
        sample_rate = 16000
        output_wav = output_dir / "instant_clone.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path,
            "-ar", str(sample_rate), "-ac", "1",
            "-sample_fmt", "s16",
            str(output_wav)
        ], check=True, capture_output=True)

    @staticmethod
    def _deep_clone(audio_path: str, output_dir: Path):
        sample_rate = 16000
        output_wav = output_dir / "training_input.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path,
            "-ar", str(sample_rate), "-ac", "1",
            str(output_wav)
        ], check=True, capture_output=True)
