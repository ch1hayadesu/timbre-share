from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ParamError
from app.repositories.script_dub_repo import ScriptDubRepo
from app.repositories.voice_repo import VoiceRepo
from app.schemas.script_dub import ScriptDubVO


class ScriptDubService:
    MAX_SCRIPT_SIZE = 5 * 1024 * 1024
    MAX_ROLE_COUNT = 20

    def __init__(self, db: Session):
        self.repo = ScriptDubRepo(db)
        self.voice_repo = VoiceRepo(db)

    def create_task(
        self,
        user_id: int,
        script_text: str,
        script_name: str | None = None,
        charset: str | None = None,
        voice_mapping: dict[str, int] | None = None,
    ) -> ScriptDubVO:
        if not script_text:
            raise ParamError("剧本内容不能为空")
        if len(script_text.encode("utf-8")) > self.MAX_SCRIPT_SIZE:
            raise ParamError("剧本文件大小超限")
        if voice_mapping and len(voice_mapping) > self.MAX_ROLE_COUNT:
            raise ParamError(f"角色数量超过限制（最多{self.MAX_ROLE_COUNT}个）")

        task = self.repo.create(
            user_id=user_id,
            script_text=script_text,
            script_name=script_name,
            charset=charset,
            voice_mapping=voice_mapping,
        )
        return ScriptDubVO.model_validate(task)

    def list_tasks(self, user_id: int, page: int, page_size: int) -> tuple[list[ScriptDubVO], int]:
        items, total = self.repo.get_by_user(user_id, page, page_size)
        return [ScriptDubVO.model_validate(t) for t in items], total

    def get_task(self, task_id: int, user_id: int) -> ScriptDubVO:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("配音任务")
        if task.user_id != user_id:
            raise NotFoundError("配音任务")
        return ScriptDubVO.model_validate(task)
