import asyncio
import re
from pathlib import Path

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.repositories.script_dub_repo import ScriptDubRepo
from app.services.tts_engine import engine

LINE_RE = re.compile(r"^(.+?)[：:]\s*(.+)")

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

        emotions = [{"role": r, "dialogue": d, "emotion": "neutral"} for r, d in lines]

        audio_dir = Path(settings.data_dir, "audio")
        audio_dir.mkdir(parents=True, exist_ok=True)

        audio_segments = asyncio.run(_synthesize_all(lines, voice_mapping))

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


async def _synthesize_all(lines, voice_mapping):
    async def synth_one(role, dialogue):
        voice_id = voice_mapping.get(role, 1)
        voice_name = VOICE_MAP.get(voice_id, "zh-CN-XiaoxiaoNeural")
        return await engine.synthesize(dialogue, voice_name, 1.0, 80, 0)

    tasks = [synth_one(role, dialogue) for role, dialogue in lines]
    return await asyncio.gather(*tasks)


def _combine_audio(audio_paths: list[str], output: str):
    data = bytearray()
    for p in audio_paths:
        path = Path(p)
        if not path.exists():
            continue
        raw = path.read_bytes()
        try:
            from mutagen.mp3 import MP3
            mp3 = MP3(path)
            tag_len = len(mp3.tags) if mp3.tags else 0
            if tag_len:
                raw = raw[tag_len:]
        except Exception:
            pass
        data.extend(raw)
    if data:
        Path(output).write_bytes(bytes(data))
