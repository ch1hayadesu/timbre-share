from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Voice


class VoiceRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, voice_id: int) -> Voice | None:
        return self.db.query(Voice).filter(Voice.voice_id == voice_id).first()

    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 12,
                    keyword: str | None = None, source: str | None = None,
                    status: int | None = None):
        query = self.db.query(Voice).filter(Voice.user_id == user_id)
        if keyword:
            query = query.filter(Voice.voice_name.ilike(f"%{keyword}%"))
        if source:
            query = query.filter(Voice.source == source)
        if status is not None:
            query = query.filter(Voice.status == status)
        query = query.order_by(desc(Voice.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def get_preset_voices(self):
        return self.db.query(Voice).filter(Voice.source == "preset").all()

    def create(self, user_id: int, voice_name: str, clone_mode: int = 0,
               raw_audio_url: str | None = None,
               tts_model: str | None = None) -> Voice:
        voice = Voice(user_id=user_id, voice_name=voice_name, clone_mode=clone_mode,
                      status=0, raw_audio_url=raw_audio_url, tts_model=tts_model)
        self.db.add(voice)
        self.db.commit()
        self.db.refresh(voice)
        return voice

    def update_status(self, voice_id: int, status: int, error_message: str | None = None):
        voice = self.get_by_id(voice_id)
        if voice:
            voice.status = status
            if error_message:
                voice.error_message = error_message
                voice.retry_count = (voice.retry_count or 0) + 1
            self.db.commit()

    def update_sample_url(self, voice_id: int, sample_url: str):
        voice = self.get_by_id(voice_id)
        if voice:
            voice.sample_url = sample_url
            self.db.commit()

    def delete(self, voice_id: int, user_id: int) -> bool:
        voice = self.db.query(Voice).filter(Voice.voice_id == voice_id, Voice.user_id == user_id).first()
        if not voice:
            return False
        self.db.delete(voice)
        self.db.commit()
        return True

    def count_active_by_user(self, user_id: int) -> int:
        return self.db.query(Voice).filter(Voice.user_id == user_id, Voice.status == 1).count()

    def search_by_name(self, keyword: str, page: int = 1, page_size: int = 12):
        query = self.db.query(Voice).filter(Voice.voice_name.ilike(f"%{keyword}%")).order_by(desc(Voice.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total
