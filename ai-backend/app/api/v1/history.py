from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.repositories.history_repo import HistoryRepo
from app.repositories.favorite_repo import FavoriteRepo

router = APIRouter(prefix="/history", tags=["浏览历史"])


class ViewRequest(BaseModel):
    voice_id: int
    share_id: int | None = None


@router.post("/view")
def record_view(req: ViewRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = HistoryRepo(db)
    repo.add_view(user_id, req.voice_id, req.share_id)
    return ApiResponse.success()


@router.get("/list")
def list_history(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=50),
                 user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = HistoryRepo(db)
    items, total = repo.get_by_user(user_id, page, page_size)
    result = []
    for h in items:
        v = h.voice
        result.append({
            "id": h.id,
            "voice_id": v.voice_id if v else h.voice_id,
            "voice_name": v.voice_name if v else "已删除",
            "created_at": h.created_at.isoformat() if h.created_at else None,
        })
    return ApiResponse.success({"items": result, "total": total, "page": page, "pageSize": page_size})


@router.post("/favorite/add")
def add_favorite(req: ViewRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = FavoriteRepo(db)
    fav = repo.add(user_id, req.voice_id, req.share_id)
    return ApiResponse.success({"id": fav.id})


@router.post("/favorite/remove")
def remove_favorite(req: ViewRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = FavoriteRepo(db)
    repo.remove(user_id, req.voice_id)
    return ApiResponse.success()


@router.get("/favorite/list")
def list_favorites(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=50),
                   user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = FavoriteRepo(db)
    items, total = repo.get_by_user(user_id, page, page_size)
    result = []
    for f in items:
        v = f.voice
        result.append({
            "id": f.id,
            "voice_id": v.voice_id if v else f.voice_id,
            "voice_name": v.voice_name if v else "已删除",
            "sample_url": v.sample_url if v else None,
            "source": v.source if v else None,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        })
    return ApiResponse.success({"items": result, "total": total, "page": page, "pageSize": page_size})


@router.get("/favorite/check")
def check_favorite(voice_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = FavoriteRepo(db)
    return ApiResponse.success({"favorited": repo.is_favorited(user_id, voice_id)})
