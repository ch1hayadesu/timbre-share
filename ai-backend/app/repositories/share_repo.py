from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models import VoiceShare, VoiceDownload, Voice


class ShareRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_share_by_voice(self, voice_id: int) -> VoiceShare | None:
        return self.db.query(VoiceShare).filter(VoiceShare.voice_id == voice_id).first()

    def get_share_by_id(self, share_id: int) -> VoiceShare | None:
        return self.db.query(VoiceShare).filter(VoiceShare.share_id == share_id).first()

    def create_share(self, voice_id: int, user_id: int, tags: str | None = None) -> VoiceShare:
        share = VoiceShare(voice_id=voice_id, user_id=user_id, tags=tags)
        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def update_status(self, share_id: int, status: int):
        share = self.get_share_by_id(share_id)
        if share:
            share.status = status
            self.db.commit()

    def list_public(self, keyword: str | None, page: int = 1, page_size: int = 12):
        query = self.db.query(VoiceShare).options(joinedload(VoiceShare.voice)).filter(VoiceShare.status == 1)
        if keyword:
            query = query.join(Voice).filter(Voice.voice_name.ilike(f"%{keyword}%"))
        query = query.order_by(desc(VoiceShare.download_count), desc(VoiceShare.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def record_download(self, share_id: int, user_id: int, voice_id: int) -> VoiceDownload:
        download = VoiceDownload(share_id=share_id, user_id=user_id, voice_id=voice_id)
        self.db.add(download)
        self.db.query(VoiceShare).filter(VoiceShare.share_id == share_id).update(
            {VoiceShare.download_count: VoiceShare.download_count + 1}
        )
        self.db.commit()
        self.db.refresh(download)
        return download

    def get_downloads_by_user(self, user_id: int, page: int = 1, page_size: int = 12):
        query = self.db.query(VoiceDownload).filter(VoiceDownload.user_id == user_id).order_by(desc(VoiceDownload.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total
