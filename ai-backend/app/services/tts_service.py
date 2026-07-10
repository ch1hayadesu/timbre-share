from __future__ import annotations
import asyncio
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import NotFoundError, ForbiddenError, ParamError
from app.repositories.tts_repo import TtsRepo
from app.repositories.voice_repo import VoiceRepo
from app.schemas.tts import TtsRecordVO, TtsRequest
from app.services import tts_engine


VOICE_MAP = {
    1: "zh-CN-XiaoxiaoNeural",
    2: "zh-CN-YunxiNeural",
    3: "zh-CN-XiaoyiNeural",
    4: "zh-CN-YunjianNeural",
    5: "zh-CN-XiaohanNeural",
}


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
            tts_model=req.model,
        )
        # Run TTS synchronously (no Celery/Redis available in dev)
        self._run_synthesis(record, req)
        self.repo.db.refresh(record)
        return TtsRecordVO.model_validate(record)

    def _run_synthesis(self, record, req):
        voice_name = VOICE_MAP.get(req.voice_id, "zh-CN-XiaoxiaoNeural")
        try:
            self.repo.update_status(record.record_id, 2)
            self.repo.db.commit()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                tts_engine.synthesize(
                    text=req.text,
                    voice_name=voice_name,
                    speed=req.speed,
                    volume=req.volume,
                    pitch=req.pitch,
                    model=req.model or "edge-tts",
                )
            )
            loop.close()
            audio_dir = Path(settings.data_dir, "audio")
            rel_path = Path(result.audio_path).relative_to(audio_dir).as_posix()
            self.repo.update_audio(record.record_id, rel_path)
            self.repo.db.commit()
        except Exception as exc:
            self.repo.update_status(record.record_id, -1, str(exc))
            self.repo.db.commit()

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

    def get_available_models(self) -> list[dict]:
        return tts_engine.get_available_models()
