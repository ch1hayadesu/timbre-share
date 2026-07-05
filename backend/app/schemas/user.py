from datetime import datetime

from pydantic import BaseModel


class UserVO(BaseModel):
    user_id: int
    phone: str
    membership_level: int
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    token: str
    user: UserVO
