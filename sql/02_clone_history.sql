-- ============================================================
-- 克隆历史记录表（独立于 voice 表，删除音色不影响此记录）
-- 执行: mysql -u root -p timbre_share < 02_clone_history.sql
-- ============================================================

USE timbre_share;

CREATE TABLE IF NOT EXISTS clone_history (
    id               BIGINT          AUTO_INCREMENT PRIMARY KEY,
    voice_id         BIGINT          DEFAULT NULL COMMENT '原音色ID（删除后为NULL）',
    user_id          BIGINT          NOT NULL COMMENT '所属用户',
    voice_name       VARCHAR(100)    NOT NULL COMMENT '克隆时的音色名称',
    clone_mode       TINYINT         NOT NULL DEFAULT 0 COMMENT '0:即时克隆 1:深度克隆',
    model_path       VARCHAR(500)    DEFAULT NULL COMMENT '模型文件路径',
    sample_url       VARCHAR(500)    DEFAULT NULL COMMENT '试听音频路径',
    status           TINYINT         NOT NULL DEFAULT 0 COMMENT '0:处理中 1:就绪 2:失败',
    error_message    VARCHAR(500)    DEFAULT NULL COMMENT '失败原因',
    tts_model        VARCHAR(50)     DEFAULT NULL COMMENT '使用的TTS模型',
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_clone_history_user_id (user_id),
    INDEX idx_clone_history_status (status),
    INDEX idx_clone_history_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='克隆历史记录表（独立于voice表，删除音色不影响此记录）';

ALTER TABLE clone_history ADD CONSTRAINT fk_clone_history_user
    FOREIGN KEY (user_id) REFERENCES `user`(user_id);
