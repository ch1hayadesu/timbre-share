from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ForbiddenError, ParamError
from app.repositories.tts_repo import TtsRepo
from app.repositories.voice_repo import VoiceRepo
from app.schemas.tts import TtsRecordVO, TtsRequest
from app.tasks.tts_tasks import synthesize_tts


class TtsService:
    MAX_TEXT_LENGTH = 1000

    def __init__(self, db: Session):
        self.repo = TtsRepo(db)
        self.voice_repo = VoiceRepo(db)

    def synthesize(self, user_id: int, req: TtsRequest) -> TtsRecordVO:
        voice = self.voice_repo.get_by_id(req.voice_id)
        if not voice:
            raise NotFoundError("音色")
        if voice.user_id != user_id and voice.source not in ("preset", "shared"):
            raise ForbiddenError("无权使用该音色")
        if voice.status != 1:
            raise ParamError("音色尚未就绪")
        if len(req.text) > self.MAX_TEXT_LENGTH:
            raise ParamError(f"TTS文本超出{self.MAX_TEXT_LENGTH}字限制")

        record = self.repo.create(
            user_id=user_id,
            voice_id=req.voice_id,
            text=req.text,
            speed=req.speed,
            volume=req.volume,
            pitch=req.pitch,
            engine_name=req.engine,
        )
        synthesize_tts.delay(
            record_id=record.record_id,
            text=req.text,
            voice_id=req.voice_id,
            speed=req.speed,
            volume=req.volume,
            pitch=req.pitch,
            engine=req.engine,
        )
        return TtsRecordVO.model_validate(record)

    def list_history(self, user_id: int, page: int, page_size: int) -> tuple[list[TtsRecordVO], int]:
        items, total = self.repo.get_by_user(user_id, page, page_size)
        return [TtsRecordVO.model_validate(r) for r in items], total

    def get_record(self, record_id: int, user_id: int) -> TtsRecordVO:
        record = self.repo.get_by_id(record_id)
        if not record:
            raise NotFoundError("合成记录")
        if record.user_id != user_id:
            raise ForbiddenError()
        return TtsRecordVO.model_validate(record)
