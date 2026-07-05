from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.schemas.tts import TtsRequest
from app.services.tts_service import TtsService

router = APIRouter(prefix="/tts", tags=["TTS合成模块"])


@router.post("/synthesize")
def synthesize(
    req: TtsRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    result = svc.synthesize(user_id, req)
    return ApiResponse.success(result.model_dump())


@router.get("/history")
def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    items, total = svc.list_history(user_id, page, page_size)
    return ApiResponse.paginated([r.model_dump() for r in items], total, page, page_size)


@router.get("/record/{record_id}")
def get_record(
    record_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    return ApiResponse.success(svc.get_record(record_id, user_id).model_dump())
