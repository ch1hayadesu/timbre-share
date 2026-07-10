from __future__ import annotations
import random

from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import NotFoundError, ParamError
from app.repositories.user_repo import UserRepo
from app.repositories.notification_repo import NotificationRepo
from app.schemas.user import UserVO, LoginResponse


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepo(db)
        self.notify_repo = NotificationRepo(db)

    def send_code(self, phone: str):
        if not phone or len(phone) < 11:
            raise ParamError("手机号格式不正确")
        if settings.sms_enabled:
            code = str(random.randint(100000, 999999))
            # TODO: integrate SMS provider
            pass
        return {"message": "验证码已发送"}

    def login(self, phone: str, code: str) -> LoginResponse:
        if not phone or len(phone) < 11:
            raise ParamError("手机号格式不正确")
        if not code or len(code) != 6:
            raise ParamError("验证码格式不正确")
        # MVP: code validation is mocked
        user = self.repo.get_by_phone(phone)
        if not user:
            user = self.repo.create(phone)
        token = str(user.user_id)
        return LoginResponse(token=token, user=UserVO.model_validate(user))

    def get_profile(self, user_id: int) -> UserVO:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("用户")
        return UserVO.model_validate(user)
