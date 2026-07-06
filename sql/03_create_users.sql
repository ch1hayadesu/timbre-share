-- ============================================================
-- 音色共享平台 — MySQL 8.0 用户权限配置
-- 引擎: InnoDB  字符集: utf8mb4  排序: utf8mb4_unicode_ci
-- 执行: 以 root 连接后 source 本文件
-- ============================================================

-- 密码仅在首次初始化时明文展示，交付后立即修改
-- ============================================================
-- 1. 应用用户（Java Spring Boot 后端使用）
--    权限: 业务表 CRUD（无 DDL）
-- ============================================================
CREATE USER IF NOT EXISTS 'app_user'@'127.0.0.1'
    IDENTIFIED WITH caching_sha2_password BY 'App@2026Timbre!';
CREATE USER IF NOT EXISTS 'app_user'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'App@2026Timbre!';

GRANT SELECT, INSERT, UPDATE, DELETE ON timbre_share.* TO 'app_user'@'127.0.0.1';
GRANT SELECT, INSERT, UPDATE, DELETE ON timbre_share.* TO 'app_user'@'localhost';

-- ============================================================
-- 2. 只读用户（报表/监控使用）
--    权限: 仅 SELECT
-- ============================================================
CREATE USER IF NOT EXISTS 'readonly_user'@'127.0.0.1'
    IDENTIFIED WITH caching_sha2_password BY 'ReadOnly@2026!';
CREATE USER IF NOT EXISTS 'readonly_user'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'ReadOnly@2026!';
CREATE USER IF NOT EXISTS 'readonly_user'@'%'
    IDENTIFIED WITH caching_sha2_password BY 'ReadOnly@2026!';

GRANT SELECT ON timbre_share.* TO 'readonly_user'@'127.0.0.1';
GRANT SELECT ON timbre_share.* TO 'readonly_user'@'localhost';
GRANT SELECT ON timbre_share.* TO 'readonly_user'@'%';

-- ============================================================
-- 3. 管理用户（DBA 运维使用）
--    权限: 全部权限含 GRANT，限本地连接
-- ============================================================
CREATE USER IF NOT EXISTS 'admin_user'@'127.0.0.1'
    IDENTIFIED WITH caching_sha2_password BY 'Admin@2026Timbre!';
CREATE USER IF NOT EXISTS 'admin_user'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'Admin@2026Timbre!';

GRANT ALL PRIVILEGES ON timbre_share.* TO 'admin_user'@'127.0.0.1' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON timbre_share.* TO 'admin_user'@'localhost' WITH GRANT OPTION;

-- ============================================================
-- 刷新权限
-- ============================================================
FLUSH PRIVILEGES;

-- ============================================================
-- 验证
-- ============================================================
SELECT user, host, plugin AS authentication_plugin
FROM mysql.user
WHERE user IN ('app_user', 'readonly_user', 'admin_user')
ORDER BY user;
