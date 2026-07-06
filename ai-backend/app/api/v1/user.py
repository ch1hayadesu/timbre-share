from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.schemas.common import PhoneRequest, VerifyCodeRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["用户模块"])


@router.post("/send-code")
def send_code(req: PhoneRequest, db: Session = Depends(get_db)):
    svc = UserService(db)
    result = svc.send_code(req.phone)
    return ApiResponse.success(result)


@router.post("/login")
def login(req: VerifyCodeRequest, db: Session = Depends(get_db)):
    svc = UserService(db)
    result = svc.login(req.phone, req.code)
    return ApiResponse.success(result.model_dump(mode='json'))


@router.get("/profile")
def get_profile(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    svc = UserService(db)
    return ApiResponse.success(svc.get_profile(user_id).model_dump(mode='json'))
