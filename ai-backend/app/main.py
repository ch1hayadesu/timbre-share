from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.core.exceptions import AppException
from app.core.response import app_exception_handler
from app.api.v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(settings.data_dir, "audio", "tts").mkdir(parents=True, exist_ok=True)
    Path(settings.data_dir, "audio", "uploads").mkdir(parents=True, exist_ok=True)
    Path(settings.data_dir, "models").mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="音色共享平台 API",
    description="Voice Sharing Platform - Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated audio files
audio_dir = Path(settings.data_dir, "audio")
audio_dir.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")

app.include_router(v1_router)
app.add_exception_handler(AppException, app_exception_handler)


@app.get("/health")
def health():
    return {"status": "ok"}
