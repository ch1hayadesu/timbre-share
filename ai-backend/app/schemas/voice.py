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
    created_at: datetime

    model_config = {"from_attributes": True}


class CloneRequest(BaseModel):
    voice_name: str
    clone_mode: int = 0


class VoiceNameUpdate(BaseModel):
    voice_name: str
