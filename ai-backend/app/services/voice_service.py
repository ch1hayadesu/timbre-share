from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import NotFoundError, ForbiddenError, ParamError
from app.repositories.voice_repo import VoiceRepo
from app.schemas.voice import VoiceVO
from app.tasks.clone_tasks import process_clone_task


class VoiceService:
    def __init__(self, db: Session):
        self.repo = VoiceRepo(db)

    def list_voices(self, user_id: int, page: int, page_size: int,
                    keyword: str | None = None, source: str | None = None,
                    status: int | None = None) -> tuple[list[VoiceVO], int]:
        items, total = self.repo.get_by_user(user_id, page, page_size, keyword, source, status)
        return [VoiceVO.model_validate(v) for v in items], total

    def get_voice(self, voice_id: int, user_id: int) -> VoiceVO:
        voice = self.repo.get_by_id(voice_id)
        if not voice:
            raise NotFoundError("音色")
        if voice.user_id != user_id and voice.source != "preset":
            raise ForbiddenError("无权访问该音色")
        return VoiceVO.model_validate(voice)

    def create_clone_task(self, user_id: int, voice_name: str, clone_mode: int = 0,
                          raw_audio_url: str | None = None) -> VoiceVO:
        if not voice_name or len(voice_name) > 100:
            raise ParamError("音色名称不合法")
        if self.repo.count_active_by_user(user_id) >= 10:
            raise ParamError("音色数量已达上限（10个）")
        voice = self.repo.create(user_id=user_id, voice_name=voice_name, clone_mode=clone_mode,
                                 raw_audio_url=raw_audio_url)
        if raw_audio_url:
            audio_path = str(Path(settings.data_dir, "audio", raw_audio_url))
        else:
            audio_path = ""
        process_clone_task.delay(
            voice_id=voice.voice_id,
            audio_path=audio_path,
            clone_mode=clone_mode,
        )
        return VoiceVO.model_validate(voice)

    def update_voice_name(self, voice_id: int, user_id: int, voice_name: str) -> VoiceVO:
        voice = self.repo.get_by_id(voice_id)
        if not voice:
            raise NotFoundError("音色")
        if voice.user_id != user_id:
            raise ForbiddenError()
        if not voice_name or len(voice_name) > 100:
            raise ParamError("音色名称不合法")
        voice.voice_name = voice_name
        return VoiceVO.model_validate(voice)

    def delete_voice(self, voice_id: int, user_id: int):
        if not self.repo.delete(voice_id, user_id):
            raise NotFoundError("音色")

    def get_presets(self) -> list[VoiceVO]:
        voices = self.repo.get_preset_voices()
        return [VoiceVO.model_validate(v) for v in voices]
