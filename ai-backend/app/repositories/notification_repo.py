from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Notification


class NotificationRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 12):
        query = self.db.query(Notification).filter(Notification.user_id == user_id).order_by(desc(Notification.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def count_unread(self, user_id: int) -> int:
        return self.db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).count()

    def mark_read(self, notify_id: int, user_id: int):
        self.db.query(Notification).filter(
            Notification.notify_id == notify_id, Notification.user_id == user_id
        ).update({"is_read": True})
        self.db.commit()

    def mark_all_read(self, user_id: int):
        self.db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update(
            {"is_read": True}
        )
        self.db.commit()

    def create(self, user_id: int, title: str, content: str | None = None, type: int = 0) -> Notification:
        n = Notification(user_id=user_id, title=title, content=content, type=type)
        self.db.add(n)
        self.db.commit()
        self.db.refresh(n)
        return n
