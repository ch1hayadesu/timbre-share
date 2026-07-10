from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel


class ShareRequest(BaseModel):
    tags: str | None = None


class SharedVoiceVO(BaseModel):
    share_id: int
    voice_id: int
    voice_name: str
    user_id: int
    download_count: int
    tags: str | None = None
    sample_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
