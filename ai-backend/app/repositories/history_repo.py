from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import VoiceBrowseHistory


class HistoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def add_view(self, user_id: int, voice_id: int, share_id: int | None = None) -> VoiceBrowseHistory:
        record = VoiceBrowseHistory(user_id=user_id, voice_id=voice_id, share_id=share_id)
        self.db.add(record)
        self.db.commit()
        return record

    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 20):
        query = self.db.query(VoiceBrowseHistory).filter(
            VoiceBrowseHistory.user_id == user_id
        ).order_by(desc(VoiceBrowseHistory.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total
