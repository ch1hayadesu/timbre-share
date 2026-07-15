-- ============================================================
-- 音色共享平台 - 运维管理后台种子数据
-- 创建默认管理员账号
-- ============================================================

-- 默认管理员: admin / admin123
-- 密码为 admin123 的 SHA-256 哈希值
-- 可通过 Python 生成: hashlib.sha256("admin123".encode()).hexdigest()

INSERT INTO `user` (`phone`, `membership_level`, `role`, `is_disabled`, `created_at`)
VALUES ('00000000000', 0, 'admin', 0, NOW());
