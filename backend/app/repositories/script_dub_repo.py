from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import ScriptDubTask


class ScriptDubRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, task_id: int) -> ScriptDubTask | None:
        return self.db.query(ScriptDubTask).filter(ScriptDubTask.task_id == task_id).first()

    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 12):
        query = self.db.query(ScriptDubTask).filter(ScriptDubTask.user_id == user_id).order_by(desc(ScriptDubTask.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(
        self,
        user_id: int,
        script_text: str,
        script_name: str | None = None,
        charset: str | None = None,
        voice_mapping: dict[str, int] | None = None,
    ) -> ScriptDubTask:
        task = ScriptDubTask(
            user_id=user_id,
            script_text=script_text,
            script_name=script_name,
            charset=charset,
            role_count=len(voice_mapping) if voice_mapping else 0,
            voice_mapping=voice_mapping,
            status=0,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_emotion_result(self, task_id: int, emotion_result: Any):
        task = self.get_by_id(task_id)
        if task:
            task.emotion_result = emotion_result
            self.db.commit()

    def update_output(self, task_id: int, output_url: str):
        task = self.get_by_id(task_id)
        if task:
            task.output_url = output_url
            task.status = 1
            self.db.commit()
