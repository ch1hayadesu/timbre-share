from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import TtsRecord


class TtsRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, record_id: int) -> TtsRecord | None:
        return self.db.query(TtsRecord).filter(TtsRecord.record_id == record_id).first()

    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 12):
        query = self.db.query(TtsRecord).filter(TtsRecord.user_id == user_id).order_by(desc(TtsRecord.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(
        self, user_id: int, voice_id: int, text: str, speed: float, volume: int, pitch: int,
        engine_name: str | None = None,
    ) -> TtsRecord:
        record = TtsRecord(
            user_id=user_id,
            voice_id=voice_id,
            text=text,
            text_length=len(text),
            speed=speed,
            volume=volume,
            pitch=pitch,
            engine_name=engine_name,
            status=0,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_audio(self, record_id: int, audio_url: str):
        record = self.get_by_id(record_id)
        if record:
            record.audio_url = audio_url
            record.status = 1
            self.db.commit()

    def update_status(self, record_id: int, status: int, error_message: str | None = None):
        record = self.get_by_id(record_id)
        if record:
            record.status = status
            if error_message:
                record.error_message = error_message
            self.db.commit()
