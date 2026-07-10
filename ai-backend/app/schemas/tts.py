from datetime import datetime

from pydantic import BaseModel, Field


class TtsRequest(BaseModel):
    voice_id: int
    text: str = Field(..., min_length=1, max_length=1000)
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    volume: int = Field(default=80, ge=0, le=100)
    pitch: int = Field(default=0, ge=-12, le=12)
    engine: str | None = None


class TtsRecordVO(BaseModel):
    record_id: int
    user_id: int
    voice_id: int
    text: str
    text_length: int
    speed: float
    volume: int
    pitch: int
    engine_name: str | None = None
    audio_url: str | None = None
    status: int
    created_at: datetime

    model_config = {"from_attributes": True}
