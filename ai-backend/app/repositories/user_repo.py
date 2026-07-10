from __future__ import annotations
from sqlalchemy.orm import Session

from app.models import User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_by_phone(self, phone: str) -> User | None:
        return self.db.query(User).filter(User.phone == phone).first()

    def create(self, phone: str) -> User:
        user = User(phone=phone)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
