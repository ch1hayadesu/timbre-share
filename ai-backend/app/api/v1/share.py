import asyncio
from pathlib import Path

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id, get_optional_user_id
from app.config import settings
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
    return ApiResponse.success(result.model_dump(mode='json'))


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
    return ApiResponse.paginated([s.model_dump(mode='json') for s in items], total, page, page_size)


@router.post("/download/{share_id}")
def download_voice(
    share_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    result = svc.download_voice(share_id, user_id)
    return ApiResponse.success(result.model_dump(mode='json'))


VOICE_MAP = {
    1: "zh-CN-XiaoxiaoNeural",
    2: "zh-CN-YunxiNeural",
    3: "zh-CN-XiaoyiNeural",
    4: "zh-CN-YunjianNeural",
    5: "zh-CN-YunxiaNeural",
    6: "zh-CN-YunyangNeural",
    7: "zh-CN-liaoning-XiaobeiNeural",
}

PREVIEW_TEXT = "你好，这是我在音色共享平台的声音样本，欢迎收听。"

@router.get("/preview/{share_id}")
def preview_voice(
    share_id: int,
    db: Session = Depends(get_db),
):
    from app.services.tts_engine import engine as tts_engine

    svc = ShareService(db)
    share = svc.repo.get_share_by_id(share_id)
    if not share or share.status != 1:
        return ApiResponse.error(10002, "分享记录不存在")

    voice = share.voice
    tts_name = VOICE_MAP.get(voice.voice_id)
    if not tts_name:
        return ApiResponse.error(10002, "该音色暂不支持试听")

    preview_dir = Path(settings.data_dir, "audio", "preview")
    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_path = preview_dir / f"preview_{share_id}.mp3"

    if not preview_path.exists():
        try:
            src = asyncio.run(tts_engine.synthesize(PREVIEW_TEXT, tts_name, 1.0, 80, 0))
            Path(src).rename(preview_path)
        except Exception as e:
            return ApiResponse.error(10006, f"生成试听失败: {e}")

    return FileResponse(str(preview_path), media_type="audio/mpeg")

@router.get("/my-downloads")
def list_downloads(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ShareService(db)
    items, total = svc.list_downloads(user_id, page, page_size)
    return ApiResponse.paginated([v.model_dump(mode='json') for v in items], total, page, page_size)
