from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel


class VoiceVO(BaseModel):
    voice_id: int
    user_id: int
    voice_name: str
    clone_mode: int
    status: int
    source: str
    model_path: str | None = None
    sample_url: str | None = None
    raw_audio_url: str | None = None
    error_message: str | None = None
    retry_count: int = 0
    tts_model: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CloneRequest(BaseModel):
    voice_name: str
    clone_mode: int = 0
    model: str | None = None


class VoiceNameUpdate(BaseModel):
    voice_name: str
