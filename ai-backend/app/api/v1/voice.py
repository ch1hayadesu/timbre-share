from __future__ import annotations
from pathlib import Path
import uuid

from fastapi import APIRouter, Depends, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.schemas.voice import VoiceNameUpdate
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["音色管理模块"])


@router.get("/list")
def list_voices(
    keyword: str | None = Query(None),
    source: str | None = Query(None),
    status: int | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    items, total = svc.list_voices(user_id, page, page_size, keyword, source, status)
    return ApiResponse.paginated([v.model_dump(mode='json') for v in items], total, page, page_size)


@router.get("/presets")
def get_presets(db: Session = Depends(get_db)):
    svc = VoiceService(db)
    voices = svc.get_presets()
    return ApiResponse.success([v.model_dump(mode='json') for v in voices])


@router.get("/detail/{voice_id}")
def get_voice(
    voice_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    return ApiResponse.success(svc.get_voice(voice_id, user_id).model_dump(mode='json'))


@router.post("/clone")
async def create_clone(
    file: UploadFile,
    voice_name: str = Form(...),
    clone_mode: int = Form(0),
    model: str | None = Form(None),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    upload_dir = Path(settings.data_dir, "audio", "uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename).suffix if file.filename else ".wav"
    dest = upload_dir / f"clone_{user_id}_{uuid.uuid4().hex}{ext}"
    content = await file.read()
    dest.write_bytes(content)
    raw_url = f"uploads/{dest.name}"

    svc = VoiceService(db)
    result = await svc.create_clone_task(user_id, voice_name, clone_mode, raw_url, model)
    return ApiResponse.success(result.model_dump(mode='json'))


@router.patch("/update/{voice_id}")
def update_voice_name(
    voice_id: int,
    req: VoiceNameUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    result = svc.update_voice_name(voice_id, user_id, req.voice_name)
    return ApiResponse.success(result.model_dump(mode='json'))


@router.delete("/delete/{voice_id}")
def delete_voice(
    voice_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = VoiceService(db)
    svc.delete_voice(voice_id, user_id)
    return ApiResponse.success()
