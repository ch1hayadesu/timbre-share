from __future__ import annotations
from datetime import datetime
from typing import Any, Optional, Dict

from pydantic import BaseModel, Field


class ScriptDubRequest(BaseModel):
    script_name: Optional[str] = None
    script_text: str = Field(..., min_length=1)
    charset: Optional[str] = None
    voice_mapping: Optional[Dict[str, int]] = None


class ScriptDubVO(BaseModel):
    task_id: int
    user_id: int
    script_name: Optional[str] = None
    script_text: str
    charset: Optional[str] = None
    role_count: int
    voice_mapping: Any = None
    emotion_result: Any = None
    output_url: Optional[str] = None
    status: int
    error_message: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
