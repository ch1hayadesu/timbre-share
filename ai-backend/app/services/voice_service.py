from __future__ import annotations
import os
import shutil
import subprocess
import wave
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import NotFoundError, ForbiddenError, ParamError
from app.repositories.voice_repo import VoiceRepo
from app.schemas.voice import VoiceVO
from app.services import tts_engine


class VoiceService:
    def __init__(self, db: Session):
        self.repo = VoiceRepo(db)

    def list_voices(self, user_id: int, page: int, page_size: int,
                    keyword: str | None = None, source: str | None = None,
                    status: int | None = None) -> tuple[list[VoiceVO], int]:
        items, total = self.repo.get_by_user(user_id, page, page_size, keyword, source, status)
        return [VoiceVO.model_validate(v) for v in items], total

    def get_voice(self, voice_id: int, user_id: int) -> VoiceVO:
        voice = self.repo.get_by_id(voice_id)
        if not voice:
            raise NotFoundError("音色")
        if voice.user_id != user_id and voice.source != "preset":
            raise ForbiddenError("无权访问该音色")
        return VoiceVO.model_validate(voice)

    async def create_clone_task(self, user_id: int, voice_name: str, clone_mode: int = 0,
                                raw_audio_url: str | None = None,
                                tts_model: str | None = None) -> VoiceVO:
        if not voice_name or len(voice_name) > 100:
            raise ParamError("音色名称不合法")
        if self.repo.count_active_by_user(user_id) >= 10:
            raise ParamError("音色数量已达上限（10个）")
        voice = self.repo.create(user_id=user_id, voice_name=voice_name, clone_mode=clone_mode,
                                 raw_audio_url=raw_audio_url, tts_model=tts_model)
        await self._process_clone(voice, raw_audio_url, clone_mode, tts_model or "edge-tts")
        return VoiceVO.model_validate(voice)

    async def _process_clone(self, voice, audio_path: str | None, clone_mode: int, tts_model: str):
        try:
            self.repo.update_status(voice.voice_id, 2)
            self.repo.db.commit()

            models_dir = Path(settings.data_dir, "models")
            models_dir.mkdir(parents=True, exist_ok=True)
            output_dir = models_dir / f"voice_{voice.voice_id}"
            output_dir.mkdir(parents=True, exist_ok=True)

            full_audio_path = str(Path(settings.data_dir, "audio", audio_path)) if audio_path else None
            if full_audio_path and os.path.exists(full_audio_path):
                output_wav = output_dir / ("instant_clone.wav" if clone_mode == 0 else "training_input.wav")
                self._process_audio(full_audio_path, output_wav)

            sample_url = await self._generate_sample(voice.voice_id, clone_mode, tts_model)
            if sample_url:
                self.repo.update_sample_url(voice.voice_id, sample_url)
                self.repo.db.commit()

            self.repo.update_status(voice.voice_id, 1)
            self.repo.db.commit()
        except Exception as e:
            self.repo.update_status(voice.voice_id, -1, str(e))
            self.repo.db.commit()
            raise

    async def _generate_sample(self, voice_id: int, clone_mode: int, tts_model: str) -> str | None:
        try:
            voice_name = "zh-CN-XiaoxiaoNeural" if clone_mode == 0 else "zh-CN-YunxiNeural"
            demo_text = "你好，这是我克隆的音色样本，欢迎试听。"
            tts_dir = Path(settings.data_dir, "audio", "tts")
            tts_dir.mkdir(parents=True, exist_ok=True)
            output_path = tts_dir / f"clone_sample_{voice_id}.mp3"

            result = await tts_engine.synthesize(
                text=demo_text,
                voice_name=voice_name,
                speed=1.0,
                volume=80,
                pitch=0,
                model=tts_model,
            )
            shutil.copy2(result.audio_path, str(output_path))
            return f"tts/{output_path.name}"
        except Exception as e:
            print(f"[Clone] Sample generation failed: {e}")
            return None

    def update_voice_name(self, voice_id: int, user_id: int, voice_name: str) -> VoiceVO:
        voice = self.repo.get_by_id(voice_id)
        if not voice:
            raise NotFoundError("音色")
        if voice.user_id != user_id:
            raise ForbiddenError()
        if not voice_name or len(voice_name) > 100:
            raise ParamError("音色名称不合法")
        voice.voice_name = voice_name
        return VoiceVO.model_validate(voice)

    def delete_voice(self, voice_id: int, user_id: int):
        if not self.repo.delete(voice_id, user_id):
            raise NotFoundError("音色")

    def get_presets(self) -> list[VoiceVO]:
        voices = self.repo.get_preset_voices()
        return [VoiceVO.model_validate(v) for v in voices]

    @staticmethod
    def _ffmpeg_available():
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def _process_audio(audio_path: str, output_wav: Path):
        if VoiceService._ffmpeg_available():
            subprocess.run([
                "ffmpeg", "-y", "-i", audio_path,
                "-ar", "16000", "-ac", "1",
                "-sample_fmt", "s16",
                str(output_wav)
            ], check=True, capture_output=True)
            return
        shutil.copy2(audio_path, output_wav)
        try:
            with wave.open(str(output_wav), "rb") as wf:
                params = wf.getparams()
            if params.nchannels != 1 or params.framerate != 16000:
                print(f"WARNING: {output_wav.name} is {params.nchannels}ch/{params.framerate}Hz")
        except Exception:
            pass
