from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.exceptions import UnauthorizedError


def get_current_user_id(
    authorization: str = Header(None),
) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("请先登录")
    # MVP: use token as plain user_id for simplicity
    # TODO: implement real JWT validation in production
    token = authorization[7:]
    if not token.isdigit():
        raise UnauthorizedError("Token无效")
    return int(token)


def get_optional_user_id(
    authorization: str = Header(None),
) -> int | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    if not token.isdigit():
        return None
    return int(token)
