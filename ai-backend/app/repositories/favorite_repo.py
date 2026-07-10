from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import VoiceFavorite


class FavoriteRepo:
    def __init__(self, db: Session):
        self.db = db

    def add(self, user_id: int, voice_id: int, share_id: int | None = None) -> VoiceFavorite:
        existing = self.db.query(VoiceFavorite).filter(
            VoiceFavorite.user_id == user_id, VoiceFavorite.voice_id == voice_id
        ).first()
        if existing:
            return existing
        fav = VoiceFavorite(user_id=user_id, voice_id=voice_id, share_id=share_id)
        self.db.add(fav)
        self.db.commit()
        return fav

    def remove(self, user_id: int, voice_id: int) -> bool:
        fav = self.db.query(VoiceFavorite).filter(
            VoiceFavorite.user_id == user_id, VoiceFavorite.voice_id == voice_id
        ).first()
        if fav:
            self.db.delete(fav)
            self.db.commit()
            return True
        return False

    def is_favorited(self, user_id: int, voice_id: int) -> bool:
        return self.db.query(VoiceFavorite).filter(
            VoiceFavorite.user_id == user_id, VoiceFavorite.voice_id == voice_id
        ).first() is not None

    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 20):
        query = self.db.query(VoiceFavorite).filter(
            VoiceFavorite.user_id == user_id
        ).order_by(desc(VoiceFavorite.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total
