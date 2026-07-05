-- ============================================================
-- 音色共享平台 — 数据库 DDL
-- 数据库: PostgreSQL 15
-- 字符集: UTF-8
-- 版本:   V2.0
-- ============================================================

-- ============================================================
-- 0. 库与扩展
-- ============================================================
-- CREATE DATABASE timbre_share ENCODING 'UTF8';

\c timbre_share;

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- 1. 用户表
-- ============================================================
DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE "user" (
    user_id          BIGSERIAL       PRIMARY KEY,
    phone            VARCHAR(20)     NOT NULL,
    membership_level SMALLINT        NOT NULL DEFAULT 0,
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_user_phone ON "user"(phone);
CREATE INDEX idx_user_created_at ON "user"(created_at);

COMMENT ON TABLE "user" IS '用户表';
COMMENT ON COLUMN "user".phone IS '手机号，应用层加密存储';
COMMENT ON COLUMN "user".membership_level IS '会员等级 0:普通 1:高级（MVP预留）';

-- ============================================================
-- 2. 音色表
-- ============================================================
DROP TABLE IF EXISTS voice CASCADE;
CREATE TABLE voice (
    voice_id         BIGSERIAL       PRIMARY KEY,
    user_id          BIGINT          NOT NULL REFERENCES "user"(user_id),
    voice_name       VARCHAR(100)    NOT NULL,
    clone_mode       SMALLINT        NOT NULL DEFAULT 0,
    status           SMALLINT        NOT NULL DEFAULT 0,
    source           VARCHAR(20)     NOT NULL DEFAULT 'cloned',
    source_share_id  BIGINT,
    raw_audio_url    VARCHAR(500),
    model_path       VARCHAR(500),
    sample_url       VARCHAR(500),
    error_message    VARCHAR(500),
    retry_count      SMALLINT        NOT NULL DEFAULT 0,
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_voice_user_id ON voice(user_id);
CREATE INDEX idx_voice_status ON voice(status);
CREATE INDEX idx_voice_source ON voice(source);
CREATE INDEX idx_voice_created_at ON voice(created_at);
CREATE INDEX idx_voice_name_trgm ON voice USING gin(voice_name gin_trgm_ops);

COMMENT ON TABLE voice IS '音色表';
COMMENT ON COLUMN voice.clone_mode IS '0:即时克隆 1:深度克隆';
COMMENT ON COLUMN voice.status IS '0:处理中 1:就绪 2:失败';
COMMENT ON COLUMN voice.source IS 'cloned:克隆 shared:下载 preset:预设';
COMMENT ON COLUMN voice.raw_audio_url IS '用户上传的原始音频文件路径（REQ-002）';
COMMENT ON COLUMN voice.retry_count IS '克隆重试次数（REQ-006）';

-- ============================================================
-- 3. TTS合成记录表
-- ============================================================
DROP TABLE IF EXISTS tts_record CASCADE;
CREATE TABLE tts_record (
    record_id        BIGSERIAL       PRIMARY KEY,
    user_id          BIGINT          NOT NULL REFERENCES "user"(user_id),
    voice_id         BIGINT          NOT NULL REFERENCES voice(voice_id),
    text             TEXT            NOT NULL,
    text_length      INT             NOT NULL DEFAULT 0,
    speed            REAL            NOT NULL DEFAULT 1.0,
    volume           INT             NOT NULL DEFAULT 80,
    pitch            INT             NOT NULL DEFAULT 0,
    audio_url        VARCHAR(500),
    status           SMALLINT        NOT NULL DEFAULT 0,
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tts_user_id ON tts_record(user_id);
CREATE INDEX idx_tts_voice_id ON tts_record(voice_id);
CREATE INDEX idx_tts_created_at ON tts_record(created_at);

COMMENT ON TABLE tts_record IS 'TTS合成记录表';
COMMENT ON COLUMN tts_record.text_length IS '文本字数，用于统计和限流（REQ-008）';
COMMENT ON COLUMN tts_record.speed IS '语速 0.5-2.0';
COMMENT ON COLUMN tts_record.volume IS '音量 0-100';
COMMENT ON COLUMN tts_record.pitch IS '音调 -12 ~ +12 半音';
COMMENT ON COLUMN tts_record.status IS '0:处理中 1:成功 2:失败';

-- ============================================================
-- 4. 剧本配音任务表
-- ============================================================
DROP TABLE IF EXISTS script_dub_task CASCADE;
CREATE TABLE script_dub_task (
    task_id          BIGSERIAL       PRIMARY KEY,
    user_id          BIGINT          NOT NULL REFERENCES "user"(user_id),
    script_name      VARCHAR(200),
    script_text      TEXT            NOT NULL,
    charset          VARCHAR(10),
    role_count       INT             NOT NULL DEFAULT 0,
    voice_mapping    JSONB,
    emotion_result   JSONB,
    output_url       VARCHAR(500),
    status           SMALLINT        NOT NULL DEFAULT 0,
    error_message    VARCHAR(500),
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_script_dub_user_id ON script_dub_task(user_id);
CREATE INDEX idx_script_dub_status ON script_dub_task(status);
CREATE INDEX idx_script_dub_created_at ON script_dub_task(created_at);

COMMENT ON TABLE script_dub_task IS '剧本配音任务表';
COMMENT ON COLUMN script_dub_task.script_name IS '上传的剧本文件名（REQ-021）';
COMMENT ON COLUMN script_dub_task.charset IS '文件编码 UTF-8/GBK（REQ-039）';
COMMENT ON COLUMN script_dub_task.voice_mapping IS '角色→音色映射关系 JSON';
COMMENT ON COLUMN script_dub_task.emotion_result IS '逐句情感分析结果 JSON';
COMMENT ON COLUMN script_dub_task.status IS '0:处理中 1:成功 2:失败';

-- ============================================================
-- 5. 音色分享表
-- ============================================================
DROP TABLE IF EXISTS voice_share CASCADE;
CREATE TABLE voice_share (
    share_id         BIGSERIAL       PRIMARY KEY,
    voice_id         BIGINT          NOT NULL REFERENCES voice(voice_id) ON DELETE CASCADE,
    user_id          BIGINT          NOT NULL REFERENCES "user"(user_id),
    download_count   INT             NOT NULL DEFAULT 0,
    status           SMALLINT        NOT NULL DEFAULT 1,
    audit_status     SMALLINT,
    tags             VARCHAR(500),
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_voice_share_voice ON voice_share(voice_id);
CREATE INDEX idx_voice_share_user_id ON voice_share(user_id);
CREATE INDEX idx_voice_share_status ON voice_share(status);
CREATE INDEX idx_voice_share_created_at ON voice_share(created_at);
CREATE INDEX idx_voice_share_download_count ON voice_share(download_count DESC);

COMMENT ON TABLE voice_share IS '音色分享表';
COMMENT ON COLUMN voice_share.status IS '0:已下架 1:已分享';
COMMENT ON COLUMN voice_share.audit_status IS '审核状态（MVP预留）';

-- ============================================================
-- 6. 音色下载记录表
-- ============================================================
DROP TABLE IF EXISTS voice_download CASCADE;
CREATE TABLE voice_download (
    download_id      BIGSERIAL       PRIMARY KEY,
    share_id         BIGINT,
    user_id          BIGINT          NOT NULL REFERENCES "user"(user_id),
    voice_id         BIGINT          NOT NULL REFERENCES voice(voice_id),
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_voice_download_share_id ON voice_download(share_id);
CREATE INDEX idx_voice_download_user_id ON voice_download(user_id);
CREATE INDEX idx_voice_download_voice_id ON voice_download(voice_id);

COMMENT ON TABLE voice_download IS '音色下载记录表';
COMMENT ON COLUMN voice_download.share_id IS '分享ID，分享者删除音色后可为NULL，已下载用户不受影响';

-- ============================================================
-- 7. 验证码表
-- ============================================================
DROP TABLE IF EXISTS verification_code CASCADE;
CREATE TABLE verification_code (
    id               BIGSERIAL       PRIMARY KEY,
    phone            VARCHAR(20)     NOT NULL,
    code             VARCHAR(6)      NOT NULL,
    purpose          SMALLINT        NOT NULL DEFAULT 0,
    expires_at       TIMESTAMP       NOT NULL,
    used             BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_verification_code_phone ON verification_code(phone);
CREATE INDEX idx_verification_code_expires ON verification_code(expires_at);

COMMENT ON TABLE verification_code IS '短信验证码表';
COMMENT ON COLUMN verification_code.purpose IS '0:注册 1:登录 2:其他';

-- ============================================================
-- 8. 通知表
-- ============================================================
DROP TABLE IF EXISTS notification CASCADE;
CREATE TABLE notification (
    notify_id        BIGSERIAL       PRIMARY KEY,
    user_id          BIGINT          NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    title            VARCHAR(200)    NOT NULL,
    content          TEXT,
    type             SMALLINT        NOT NULL DEFAULT 0,
    is_read          BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notification_user_id ON notification(user_id);
CREATE INDEX idx_notification_is_read ON notification(is_read);
CREATE INDEX idx_notification_created_at ON notification(created_at);

COMMENT ON TABLE notification IS '用户通知表';
COMMENT ON COLUMN notification.type IS '0:系统通知 1:克隆完成 2:配音完成';
