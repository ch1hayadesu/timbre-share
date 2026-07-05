from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ScriptDubRequest(BaseModel):
    script_name: str | None = None
    script_text: str = Field(..., min_length=1)
    charset: str | None = None
    voice_mapping: dict[str, int] | None = None


class ScriptDubVO(BaseModel):
    task_id: int
    user_id: int
    script_name: str | None = None
    script_text: str
    charset: str | None = None
    role_count: int
    voice_mapping: Any = None
    emotion_result: Any = None
    output_url: str | None = None
    status: int
    error_message: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
