from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.repositories.notification_repo import NotificationRepo

router = APIRouter(prefix="/notification", tags=["通知模块"])


@router.get("/list")
def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    repo = NotificationRepo(db)
    items, total = repo.get_by_user(user_id, page, page_size)
    return ApiResponse.paginated(
        [{"notify_id": n.notify_id, "title": n.title, "content": n.content, "type": n.type, "is_read": n.is_read, "created_at": n.created_at.isoformat()} for n in items],
        total,
        page,
        page_size,
    )


@router.get("/unread-count")
def unread_count(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = NotificationRepo(db)
    return ApiResponse.success({"count": repo.count_unread(user_id)})


@router.post("/mark-read/{notify_id}")
def mark_read(notify_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = NotificationRepo(db)
    repo.mark_read(notify_id, user_id)
    return ApiResponse.success()


@router.post("/mark-all-read")
def mark_all_read(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    repo = NotificationRepo(db)
    repo.mark_all_read(user_id)
    return ApiResponse.success()
