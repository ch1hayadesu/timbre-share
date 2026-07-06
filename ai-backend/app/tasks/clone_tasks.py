import os
import shutil
import subprocess
import wave
from pathlib import Path

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.repositories.voice_repo import VoiceRepo


def _ffmpeg_available():
    return shutil.which("ffmpeg") is not None


def _process_audio(audio_path: str, output_wav: Path):
    if _ffmpeg_available():
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path,
            "-ar", "16000", "-ac", "1",
            "-sample_fmt", "s16",
            str(output_wav)
        ], check=True, capture_output=True)
        return

    shutil.copy2(audio_path, output_wav)
    try:
        with wave.open(str(output_wav), "rb") as wf:
            params = wf.getparams()
        if params.nchannels != 1 or params.framerate != 16000:
            print(f"WARNING: {output_wav.name} is {params.nchannels}ch/{params.framerate}Hz, "
                  f"expected mono/16000Hz (install ffmpeg for proper resampling)")
    except Exception:
        pass


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

        output_wav = output_dir / ("instant_clone.wav" if clone_mode == 0 else "training_input.wav")
        _process_audio(audio_path, output_wav)

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
