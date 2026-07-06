import asyncio
import re
import tempfile
from pathlib import Path

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.repositories.script_dub_repo import ScriptDubRepo
from app.services.tts_engine import engine

LINE_RE = re.compile(r"^(.+?)[：:]\s*(.+)")


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def process_dub_task(self, task_id: int):
    db = SessionLocal()
    try:
        repo = ScriptDubRepo(db)
        task = repo.get_by_id(task_id)
        if not task:
            return {"error": "task not found"}

        voice_mapping = task.voice_mapping or {}
        lines = []
        for line_text in task.script_text.strip().split("\n"):
            m = LINE_RE.match(line_text.strip())
            if m:
                lines.append((m.group(1).strip(), m.group(2).strip()))

        if not lines:
            repo.update_emotion_result(task_id, [])
            repo.update_output(task_id, "")
            return {"task_id": task_id, "lines": 0}

        emotions = []
        audio_segments = []
        audio_dir = Path(settings.data_dir, "audio")
        audio_dir.mkdir(parents=True, exist_ok=True)

        for role, dialogue in lines:
            voice_id = voice_mapping.get(role, 1)
            voice_name = _resolve_voice_name(voice_id)
            emotions.append({"role": role, "dialogue": dialogue, "emotion": "neutral"})

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                abs_path = loop.run_until_complete(
                    engine.synthesize(dialogue, voice_name, 1.0, 80, 0)
                )
                audio_segments.append(abs_path)
            finally:
                loop.close()

        repo.update_emotion_result(task_id, emotions)

        output_path = audio_dir / f"dub_{task_id}.mp3"
        _combine_audio(audio_segments, str(output_path))

        rel_path = output_path.relative_to(audio_dir).as_posix()
        repo.update_output(task_id, rel_path)
        return {"task_id": task_id, "output_url": rel_path, "lines": len(lines)}

    except Exception as exc:
        db.rollback()
        try:
            repo = ScriptDubRepo(db)
            task = repo.get_by_id(task_id)
            if task:
                task.status = -1
                task.error_message = str(exc)
                db.commit()
        except Exception:
            db.rollback()
        raise self.retry(exc=exc)

    finally:
        db.close()


def _resolve_voice_name(voice_id: int) -> str:
    VOICE_MAP = {
        1: "zh-CN-XiaoxiaoNeural",
        2: "zh-CN-YunxiNeural",
        3: "zh-CN-XiaoyiNeural",
        4: "zh-CN-YunjianNeural",
        5: "zh-CN-XiaohanNeural",
    }
    return VOICE_MAP.get(voice_id, "zh-CN-XiaoxiaoNeural")


def _combine_audio(audio_paths: list[str], output: str):
    import wave

    if not audio_paths:
        return

    frames = []
    params = None
    for p in audio_paths:
        p = p.replace(".mp3", ".wav") if not p.endswith(".wav") else p
        if not Path(p).exists():
            continue
        with wave.open(p, "rb") as w:
            if params is None:
                params = w.getparams()
            frames.append(w.readframes(w.getnframes()))

    if not frames:
        return

    with wave.open(output.replace(".mp3", ".wav"), "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames))
