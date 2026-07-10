from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import ApiResponse
from app.core.dependencies import get_current_user_id
from app.database import get_db
from app.schemas.script_dub import ScriptDubRequest
from app.services.script_dub_service import ScriptDubService

router = APIRouter(prefix="/script-dub", tags=["剧本配音模块"])


@router.post("/create")
def create_task(
    req: ScriptDubRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ScriptDubService(db)
    result = svc.create_task(
        user_id=user_id,
        script_text=req.script_text,
        script_name=req.script_name,
        charset=req.charset,
        voice_mapping=req.voice_mapping,
    )
    return ApiResponse.success(result.model_dump(mode='json'))


@router.get("/list")
def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ScriptDubService(db)
    items, total = svc.list_tasks(user_id, page, page_size)
    return ApiResponse.paginated([t.model_dump(mode='json') for t in items], total, page, page_size)


@router.get("/detail/{task_id}")
def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    svc = ScriptDubService(db)
    return ApiResponse.success(svc.get_task(task_id, user_id).model_dump(mode='json'))
