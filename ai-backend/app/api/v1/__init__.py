from __future__ import annotations
from fastapi import APIRouter

from app.api.v1 import user, voice, tts, script_dub, share, notification, history

router = APIRouter(prefix="/api/v1")
router.include_router(user.router)
router.include_router(voice.router)
router.include_router(tts.router)
router.include_router(script_dub.router)
router.include_router(share.router)
router.include_router(notification.router)
router.include_router(history.router)
