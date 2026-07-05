from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id, get_optional_user_id
from app.database import get_db
from app.schemas.share import ShareRequest
from app.services.share_service import ShareService

router = APIRouter(prefix="/share", tags=["分享平台模块"])


@router.post("/publish/{voice_id}")
def share_voice(
    voice_id: int,
    req: ShareRequest = ShareRequest(),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    result = svc.share_voice(voice_id, user_id, req.tags)
    return ApiResponse.success(result.model_dump())


@router.post("/unpublish/{voice_id}")
def unshare_voice(
    voice_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    svc.unshare_voice(voice_id, user_id)
    return ApiResponse.success()


@router.get("/public")
def list_public(
    keyword: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    items, total = svc.list_public(keyword, page, page_size)
    return ApiResponse.paginated([s.model_dump() for s in items], total, page, page_size)


@router.post("/download/{share_id}")
def download_voice(
    share_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    result = svc.download_voice(share_id, user_id)
    return ApiResponse.success(result.model_dump())


@router.get("/my-downloads")
def list_downloads(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    items, total = svc.list_downloads(user_id, page, page_size)
    return ApiResponse.paginated([v.model_dump() for v in items], total, page, page_size)
