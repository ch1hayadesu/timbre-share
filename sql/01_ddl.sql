-- ============================================================
-- 音色共享平台 — MySQL 8.0 DDL
-- 引擎: InnoDB  字符集: utf8mb4  排序: utf8mb4_unicode_ci
-- 执行: mysql -u root -p timbre_share < 01_ddl.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS timbre_share
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE timbre_share;

-- ============================================================
-- 1. 用户表
-- ============================================================
CREATE TABLE `user` (
    user_id          BIGINT          AUTO_INCREMENT PRIMARY KEY,
    phone            VARCHAR(20)     NOT NULL COMMENT '手机号（应用层加密存储）',
    membership_level TINYINT         NOT NULL DEFAULT 0 COMMENT '会员等级 0:普通 1:高级(MVP预留)',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_user_phone (phone),
    INDEX idx_user_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ============================================================
-- 2. 音色表
-- ============================================================
CREATE TABLE voice (
    voice_id         BIGINT          AUTO_INCREMENT PRIMARY KEY,
    user_id          BIGINT          NOT NULL COMMENT '所属用户',
    voice_name       VARCHAR(100)    NOT NULL COMMENT '音色名称',
    clone_mode       TINYINT         NOT NULL DEFAULT 0 COMMENT '0:即时克隆 1:深度克隆',
    status           TINYINT         NOT NULL DEFAULT 0 COMMENT '0:处理中 1:就绪 2:失败',
    source           VARCHAR(20)     NOT NULL DEFAULT 'cloned' COMMENT 'cloned:克隆 shared:下载 preset:预设',
    source_share_id  BIGINT          DEFAULT NULL COMMENT '来源分享ID(下载时记录)',
    raw_audio_url    VARCHAR(500)    DEFAULT NULL COMMENT '用户上传原始音频路径(REQ-002)',
    model_path       VARCHAR(500)    DEFAULT NULL COMMENT '克隆模型文件路径',
    sample_url       VARCHAR(500)    DEFAULT NULL COMMENT '试听音频路径',
    error_message    VARCHAR(500)    DEFAULT NULL COMMENT '失败原因',
    retry_count      TINYINT         NOT NULL DEFAULT 0 COMMENT '克隆重试次数(REQ-006)',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_voice_user_id (user_id),
    INDEX idx_voice_status (status),
    INDEX idx_voice_source (source),
    INDEX idx_voice_created_at (created_at),
    FULLTEXT INDEX idx_voice_name_ft (voice_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='音色表';

-- ============================================================
-- 3. TTS合成记录表
-- ============================================================
CREATE TABLE tts_record (
    record_id        BIGINT          AUTO_INCREMENT PRIMARY KEY,
    user_id          BIGINT          NOT NULL COMMENT '所属用户',
    voice_id         BIGINT          NOT NULL COMMENT '使用的音色',
    text             TEXT            NOT NULL COMMENT '合成文本',
    text_length      INT             NOT NULL DEFAULT 0 COMMENT '文本字数(REQ-008)',
    speed            DECIMAL(3,1)    NOT NULL DEFAULT 1.0 COMMENT '语速 0.5-2.0',
    volume           INT             NOT NULL DEFAULT 80 COMMENT '音量 0-100',
    pitch            INT             NOT NULL DEFAULT 0 COMMENT '音调 -12~+12半音',
    audio_url        VARCHAR(500)    DEFAULT NULL COMMENT '合成音频路径',
    status           TINYINT         NOT NULL DEFAULT 0 COMMENT '0:处理中 1:成功 2:失败',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tts_user_id (user_id),
    INDEX idx_tts_voice_id (voice_id),
    INDEX idx_tts_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='TTS合成记录表';

-- ============================================================
-- 4. 剧本配音任务表
-- ============================================================
CREATE TABLE script_dub_task (
    task_id          BIGINT          AUTO_INCREMENT PRIMARY KEY,
    user_id          BIGINT          NOT NULL COMMENT '所属用户',
    script_name      VARCHAR(200)    DEFAULT NULL COMMENT '剧本文件名(REQ-021)',
    script_text      TEXT            NOT NULL COMMENT '剧本文本内容',
    charset          VARCHAR(10)     DEFAULT NULL COMMENT '文件编码 UTF-8/GBK(REQ-039)',
    role_count       INT             NOT NULL DEFAULT 0 COMMENT '角色数量',
    voice_mapping    JSON            DEFAULT NULL COMMENT '角色→音色映射关系',
    emotion_result   JSON            DEFAULT NULL COMMENT '逐句情感分析结果',
    output_url       VARCHAR(500)    DEFAULT NULL COMMENT '合成MP3路径',
    status           TINYINT         NOT NULL DEFAULT 0 COMMENT '0:处理中 1:成功 2:失败',
    error_message    VARCHAR(500)    DEFAULT NULL COMMENT '失败原因',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_script_dub_user_id (user_id),
    INDEX idx_script_dub_status (status),
    INDEX idx_script_dub_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='剧本配音任务表';

-- ============================================================
-- 5. 音色分享表
-- ============================================================
CREATE TABLE voice_share (
    share_id         BIGINT          AUTO_INCREMENT PRIMARY KEY,
    voice_id         BIGINT          NOT NULL COMMENT '被分享的音色',
    user_id          BIGINT          NOT NULL COMMENT '分享者',
    download_count   INT             NOT NULL DEFAULT 0 COMMENT '累计下载次数',
    status           TINYINT         NOT NULL DEFAULT 1 COMMENT '0:已下架 1:已分享',
    audit_status     TINYINT         DEFAULT NULL COMMENT '审核状态(MVP预留)',
    tags             VARCHAR(500)    DEFAULT NULL COMMENT '标签(逗号分隔)',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_voice_share_voice (voice_id),
    INDEX idx_voice_share_user_id (user_id),
    INDEX idx_voice_share_status (status),
    INDEX idx_voice_share_created_at (created_at),
    INDEX idx_voice_share_download_count (download_count DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='音色分享表';

-- ============================================================
-- 6. 音色下载记录表
-- ============================================================
CREATE TABLE voice_download (
    download_id      BIGINT          AUTO_INCREMENT PRIMARY KEY,
    share_id         BIGINT          DEFAULT NULL COMMENT '分享ID(分享删除后NULL，已下载用户不受影响)',
    user_id          BIGINT          NOT NULL COMMENT '下载者',
    voice_id         BIGINT          NOT NULL COMMENT '原始音色ID',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_voice_download_share_id (share_id),
    INDEX idx_voice_download_user_id (user_id),
    INDEX idx_voice_download_voice_id (voice_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='音色下载记录表';

-- ============================================================
-- 7. 验证码表
-- ============================================================
CREATE TABLE verification_code (
    id               BIGINT          AUTO_INCREMENT PRIMARY KEY,
    phone            VARCHAR(20)     NOT NULL COMMENT '手机号',
    code             VARCHAR(6)      NOT NULL COMMENT '6位验证码',
    purpose          TINYINT         NOT NULL DEFAULT 0 COMMENT '0:注册 1:登录 2:其他',
    expires_at       DATETIME        NOT NULL COMMENT '过期时间',
    used             TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否已使用',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_verification_code_phone (phone),
    INDEX idx_verification_code_expires (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='短信验证码表';

-- ============================================================
-- 8. 通知表
-- ============================================================
CREATE TABLE notification (
    notify_id        BIGINT          AUTO_INCREMENT PRIMARY KEY,
    user_id          BIGINT          NOT NULL COMMENT '目标用户',
    title            VARCHAR(200)    NOT NULL COMMENT '通知标题',
    content          TEXT            DEFAULT NULL COMMENT '通知内容',
    type             TINYINT         NOT NULL DEFAULT 0 COMMENT '0:系统通知 1:克隆完成 2:配音完成',
    is_read          TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否已读',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notification_user_id (user_id),
    INDEX idx_notification_is_read (is_read),
    INDEX idx_notification_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户通知表';

-- ============================================================
-- 外键约束
-- ============================================================
ALTER TABLE voice ADD CONSTRAINT fk_voice_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id);

ALTER TABLE tts_record ADD CONSTRAINT fk_tts_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id);
ALTER TABLE tts_record ADD CONSTRAINT fk_tts_voice
    FOREIGN KEY (voice_id) REFERENCES voice(voice_id);

ALTER TABLE script_dub_task ADD CONSTRAINT fk_script_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id);

ALTER TABLE voice_share ADD CONSTRAINT fk_share_voice
    FOREIGN KEY (voice_id) REFERENCES voice(voice_id) ON DELETE CASCADE;
ALTER TABLE voice_share ADD CONSTRAINT fk_share_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id);

ALTER TABLE voice_download ADD CONSTRAINT fk_download_share
    FOREIGN KEY (share_id) REFERENCES voice_share(share_id) ON DELETE SET NULL;
ALTER TABLE voice_download ADD CONSTRAINT fk_download_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id);
ALTER TABLE voice_download ADD CONSTRAINT fk_download_voice
    FOREIGN KEY (voice_id) REFERENCES voice(voice_id);

ALTER TABLE notification ADD CONSTRAINT fk_notify_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id) ON DELETE CASCADE;
