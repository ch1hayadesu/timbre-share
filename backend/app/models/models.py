from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, BigInteger, SmallInteger, String, Text, Float, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False, unique=True, index=True)
    membership_level = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    voices = relationship("Voice", back_populates="user")
    tts_records = relationship("TtsRecord", back_populates="user")
    script_dub_tasks = relationship("ScriptDubTask", back_populates="user")
    voice_shares = relationship("VoiceShare", back_populates="user")
    voice_downloads = relationship("VoiceDownload", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class Voice(Base):
    __tablename__ = "voice"

    voice_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    voice_name = Column(String(100), nullable=False)
    clone_mode = Column(SmallInteger, nullable=False, default=0)
    status = Column(SmallInteger, nullable=False, default=0)
    source = Column(String(20), nullable=False, default="cloned")
    source_share_id = Column(BigInteger, nullable=True)
    raw_audio_url = Column(String(500), nullable=True)
    model_path = Column(String(500), nullable=True)
    sample_url = Column(String(500), nullable=True)
    error_message = Column(String(500), nullable=True)
    retry_count = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="voices")
    tts_records = relationship("TtsRecord", back_populates="voice")
    voice_share = relationship("VoiceShare", back_populates="voice", uselist=False)
    voice_downloads = relationship("VoiceDownload", back_populates="voice")


class TtsRecord(Base):
    __tablename__ = "tts_record"

    record_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    voice_id = Column(BigInteger, ForeignKey("voice.voice_id"), nullable=False)
    text = Column(Text, nullable=False)
    text_length = Column(Integer, nullable=False, default=0)
    speed = Column(Float, nullable=False, default=1.0)
    volume = Column(Integer, nullable=False, default=80)
    pitch = Column(Integer, nullable=False, default=0)
    audio_url = Column(String(500), nullable=True)
    status = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="tts_records")
    voice = relationship("Voice", back_populates="tts_records")


class ScriptDubTask(Base):
    __tablename__ = "script_dub_task"

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    script_name = Column(String(200), nullable=True)
    script_text = Column(Text, nullable=False)
    charset = Column(String(10), nullable=True)
    role_count = Column(Integer, nullable=False, default=0)
    voice_mapping = Column(JSONB, nullable=True)
    emotion_result = Column(JSONB, nullable=True)
    output_url = Column(String(500), nullable=True)
    status = Column(SmallInteger, nullable=False, default=0)
    error_message = Column(String(500), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="script_dub_tasks")


class VoiceShare(Base):
    __tablename__ = "voice_share"

    share_id = Column(BigInteger, primary_key=True, autoincrement=True)
    voice_id = Column(BigInteger, ForeignKey("voice.voice_id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    download_count = Column(Integer, nullable=False, default=0)
    status = Column(SmallInteger, nullable=False, default=1)
    audit_status = Column(SmallInteger, nullable=True)
    tags = Column(String(500), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    voice = relationship("Voice", back_populates="voice_share")
    user = relationship("User", back_populates="voice_shares")
    voice_downloads = relationship("VoiceDownload", back_populates="voice_share")


class VoiceDownload(Base):
    __tablename__ = "voice_download"

    download_id = Column(BigInteger, primary_key=True, autoincrement=True)
    share_id = Column(BigInteger, ForeignKey("voice_share.share_id", ondelete="SET NULL"), nullable=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    voice_id = Column(BigInteger, ForeignKey("voice.voice_id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    voice_share = relationship("VoiceShare", back_populates="voice_downloads")
    user = relationship("User", back_populates="voice_downloads")
    voice = relationship("Voice", back_populates="voice_downloads")


class VerificationCode(Base):
    __tablename__ = "verification_code"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False)
    code = Column(String(6), nullable=False)
    purpose = Column(SmallInteger, nullable=False, default=0)
    expires_at = Column(TIMESTAMP, nullable=False)
    used = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notification"

    notify_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    type = Column(SmallInteger, nullable=False, default=0)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
