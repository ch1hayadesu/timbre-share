from __future__ import annotations
import asyncio
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


async def _generate_sample_audio(voice_id: int, clone_mode: int) -> str | None:
    """Generate a demo TTS sample as placeholder for cloned voice."""
    try:
        import edge_tts
        voice_name = "zh-CN-XiaoxiaoNeural" if clone_mode == 0 else "zh-CN-YunxiNeural"
        demo_text = "你好，这是我克隆的音色样本，欢迎试听。"

        tts_dir = Path(settings.data_dir, "audio", "tts")
        tts_dir.mkdir(parents=True, exist_ok=True)
        output_path = tts_dir / f"clone_sample_{voice_id}.mp3"

        communicate = edge_tts.Communicate(demo_text, voice=voice_name)
        await communicate.save(str(output_path))

        return f"tts/{output_path.name}"
    except ImportError:
        print("[CloneTask] edge-tts not installed")
        return None
    except Exception as e:
        print(f"[CloneTask] Sample generation failed: {e}")
        return None


@celery_app.task(bind=True, max_retries=1, default_retry_delay=10)
def process_clone_task(self, voice_id: int, audio_path: str, clone_mode: int):
    db = SessionLocal()
    try:
        voice_repo = VoiceRepo(db)
        voice = voice_repo.get_by_id(voice_id)
        if not voice:
            return {"error": "voice not found"}

        print(f"[CloneTask] voiceId={voice_id} start processing, clone_mode={clone_mode}")

        voice_repo.update_status(voice_id, 2)
        db.commit()

        models_dir = Path(settings.data_dir, "models")
        models_dir.mkdir(parents=True, exist_ok=True)

        output_dir = models_dir / f"voice_{voice_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        if audio_path and os.path.exists(audio_path):
            output_wav = output_dir / ("instant_clone.wav" if clone_mode == 0 else "training_input.wav")
            _process_audio(audio_path, output_wav)
            print(f"[CloneTask] voiceId={voice_id} audio processed: {output_wav.name}")
        else:
            print(f"[CloneTask] voiceId={voice_id} audio not found, skip preprocessing")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        sample_rel_path = loop.run_until_complete(_generate_sample_audio(voice_id, clone_mode))
        loop.close()

        if sample_rel_path:
            voice_repo.update_sample_url(voice_id, sample_rel_path)
            print(f"[CloneTask] voiceId={voice_id} sample_url set: {sample_rel_path}")

        voice_repo.update_status(voice_id, 1)
        db.commit()
        print(f"[CloneTask] voiceId={voice_id} completed successfully")

        return {"voice_id": voice_id, "model_path": str(output_dir), "sample_url": sample_rel_path}

    except Exception as exc:
        db.rollback()
        print(f"[CloneTask] voiceId={voice_id} failed: {exc}")
        try:
            voice_repo = VoiceRepo(db)
            voice_repo.update_status(voice_id, -1, str(exc))
            db.commit()
        except Exception:
            db.rollback()
        raise self.retry(exc=exc)

    finally:
        db.close()
