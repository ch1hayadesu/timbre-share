from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.schemas.tts import TtsRequest
from app.services.tts_service import TtsService
from app.services.tts_engine import engine as tts_engine

router = APIRouter(prefix="/tts", tags=["TTS合成模块"])


@router.post("/synthesize")
def synthesize(
    req: TtsRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    result = svc.synthesize(user_id, req)
    return ApiResponse.success(result.model_dump(mode='json'))


@router.get("/history")
def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    items, total = svc.list_history(user_id, page, page_size)
    return ApiResponse.paginated([r.model_dump(mode='json') for r in items], total, page, page_size)


@router.get("/engines")
def list_engines():
    return ApiResponse.success(tts_engine.list_engines())


@router.get("/download/{record_id}")
def download_audio(
    record_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    record = svc.get_record(record_id, user_id)
    if not record.audio_url:
        return ApiResponse.error(10002, "音频文件不存在")
    from pathlib import Path
    from app.config import settings
    fp = Path(settings.data_dir, "audio", record.audio_url)
    if not fp.exists():
        return ApiResponse.error(10002, "音频文件不存在")
    return FileResponse(str(fp), media_type="audio/mpeg", filename=f"tts_{record_id}.mp3")


@router.get("/record/{record_id}")
def get_record(
    record_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = TtsService(db)
    return ApiResponse.success(svc.get_record(record_id, user_id).model_dump(mode='json'))
