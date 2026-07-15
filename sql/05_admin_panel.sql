-- ============================================================
-- 音色共享平台 - Admin Panel Migration
-- 运维管理后台相关表及字段
-- ============================================================

-- 1. 用户表增加字段
ALTER TABLE `user` ADD COLUMN `role` VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '角色: user/admin';
ALTER TABLE `user` ADD COLUMN `is_disabled` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否被禁用';
ALTER TABLE `user` ADD COLUMN `disabled_at` DATETIME DEFAULT NULL COMMENT '禁用时间';

-- 2. 音色表增加字段
ALTER TABLE `voice` ADD COLUMN `admin_status` VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '管理状态: active/unlisted';
ALTER TABLE `voice` ADD COLUMN `is_recommended` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否推荐';
ALTER TABLE `voice` ADD COLUMN `is_popular` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否热门';
ALTER TABLE `voice` ADD COLUMN `usage_count` INT NOT NULL DEFAULT 0 COMMENT '使用次数缓存';

-- 3. 管理员操作日志表
CREATE TABLE IF NOT EXISTS `admin_operation_logs` (
    `id`             BIGINT          AUTO_INCREMENT PRIMARY KEY,
    `admin_id`       BIGINT          NOT NULL COMMENT '管理员用户ID',
    `admin_name`     VARCHAR(100)    NOT NULL COMMENT '管理员用户名',
    `operation_type` VARCHAR(50)     NOT NULL COMMENT '操作类型',
    `target_type`    VARCHAR(50)     NOT NULL COMMENT '目标类型: user/voice',
    `target_id`      BIGINT          NOT NULL COMMENT '目标ID',
    `target_name`    VARCHAR(200)    DEFAULT NULL COMMENT '目标名称',
    `result`         VARCHAR(20)     NOT NULL DEFAULT 'success' COMMENT '操作结果',
    `ip_address`     VARCHAR(50)     DEFAULT NULL COMMENT '操作IP地址',
    `detail`         TEXT            DEFAULT NULL COMMENT '操作详情JSON',
    `created_at`     DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    INDEX `idx_admin_log_admin_id` (`admin_id`),
    INDEX `idx_admin_log_op_type` (`operation_type`),
    INDEX `idx_admin_log_target_type` (`target_type`),
    INDEX `idx_admin_log_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员操作日志表';

-- 4. 系统错误日志表
CREATE TABLE IF NOT EXISTS `system_error_logs` (
    `id`              BIGINT          AUTO_INCREMENT PRIMARY KEY,
    `error_type`      VARCHAR(100)    NOT NULL COMMENT '错误类型',
    `error_message`   TEXT            NOT NULL COMMENT '错误消息',
    `traceback`       TEXT            DEFAULT NULL COMMENT '完整堆栈',
    `request_path`    VARCHAR(500)    DEFAULT NULL COMMENT '请求路径',
    `request_method`  VARCHAR(10)     DEFAULT NULL COMMENT '请求方法',
    `created_at`      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发生时间',
    INDEX `idx_err_log_type` (`error_type`),
    INDEX `idx_err_log_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统错误日志表';
