from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.schemas.voice import CloneRequest, VoiceNameUpdate
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["音色管理模块"])


@router.get("/list")
def list_voices(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    items, total = svc.list_voices(user_id, page, page_size)
    return ApiResponse.paginated([v.model_dump() for v in items], total, page, page_size)


@router.get("/presets")
def get_presets(db: Session = Depends(get_db)):
    svc = VoiceService(db)
    voices = svc.get_presets()
    return ApiResponse.success([v.model_dump() for v in voices])


@router.get("/detail/{voice_id}")
def get_voice(
    voice_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    return ApiResponse.success(svc.get_voice(voice_id, user_id).model_dump())


@router.post("/clone")
def create_clone(
    req: CloneRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    result = svc.create_clone_task(user_id, req.voice_name, req.clone_mode)
    return ApiResponse.success(result.model_dump())


@router.patch("/update/{voice_id}")
def update_voice_name(
    voice_id: int,
    req: VoiceNameUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    result = svc.update_voice_name(voice_id, user_id, req.voice_name)
    return ApiResponse.success(result.model_dump())


@router.delete("/delete/{voice_id}")
def delete_voice(
    voice_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    svc.delete_voice(voice_id, user_id)
    return ApiResponse.success()
