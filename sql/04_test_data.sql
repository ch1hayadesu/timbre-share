-- ============================================================
-- 音色共享平台 — MySQL 8.0 测试数据（三类）
-- 1. 正常数据 (Normal)  — 标识: -- [N]
-- 2. 边界数据 (Boundary) — 标识: -- [B]
-- 3. 异常数据 (Abnormal) — 标识: -- [A]
-- ============================================================

-- 允许向 AUTO_INCREMENT 列插入 0
SET @@SESSION.sql_mode = CONCAT(@@SESSION.sql_mode, ',NO_AUTO_VALUE_ON_ZERO');

-- ============================================================
-- [N] 正常数据：普通用户注册与使用
-- ============================================================
-- 用户
INSERT INTO `user` (phone, membership_level) VALUES
    ('13800138001', 0),  -- 普通用户 1
    ('13800138002', 0),  -- 普通用户 2
    ('13800138003', 1);  -- 高级会员

-- 音色克隆（即时克隆）
INSERT INTO voice (user_id, voice_name, clone_mode, status, source, raw_audio_url, model_path, sample_url) VALUES
    (1, '我的声音', 0, 1, 'cloned', '/uploads/user1/raw/voice1.wav', '/models/user1/voice1.bin', '/samples/user1/voice1.wav'),
    (2, '朗读专用', 0, 1, 'cloned', '/uploads/user2/raw/voice2.wav', '/models/user2/voice2.bin', '/samples/user2/voice2.wav');

-- 深度克隆
INSERT INTO voice (user_id, voice_name, clone_mode, status, source, raw_audio_url, model_path, sample_url) VALUES
    (3, '高保真声音', 1, 1, 'cloned', '/uploads/user3/raw/voice3.wav', '/models/user3/voice3.bin', '/samples/user3/voice3.wav');

-- TTS 合成记录
INSERT INTO tts_record (user_id, voice_id, text, text_length, speed, volume, pitch, audio_url, status) VALUES
    (1, 1, '欢迎使用音色共享平台，在这里你可以克隆自己的声音。', 28, 1.0, 80, 0, '/tts/user1/tts1.wav', 1),
    (2, 2, '今天天气真不错，适合出去散步。', 16, 1.2, 70, 2, '/tts/user2/tts2.wav', 1),
    (3, 3, '深度学习模型训练完成，音质非常好。', 18, 0.8, 90, -1, '/tts/user3/tts3.wav', 1);

-- 剧本配音任务
INSERT INTO script_dub_task (user_id, script_name, script_text, charset, role_count, voice_mapping, emotion_result, output_url, status) VALUES
    (1, '广告配音', '欢迎来到我们的产品发布会！', 'UTF-8', 1,
     '{"role1":{"voice_id":1,"name":"旁白"}}',
     '[{"text":"欢迎来到我们的产品发布会！","emotion":"热情"}]',
     '/dub/user1/script1.mp3', 1);

-- 音色分享
INSERT INTO voice_share (voice_id, user_id, tags, download_count) VALUES
    (9, 1, '男声,自然', 2),
    (10, 2, '女声,朗读', 1);

-- 音色下载
INSERT INTO voice_download (share_id, user_id, voice_id) VALUES
    (9, 2, 9),
    (9, 3, 9),
    (10, 1, 10);

-- 验证码
INSERT INTO verification_code (phone, code, purpose, expires_at) VALUES
    ('13800138001', '123456', 0, DATE_ADD(NOW(), INTERVAL 5 MINUTE));

-- 通知
INSERT INTO notification (user_id, title, content, type) VALUES
    (1, '克隆完成', '您的音色"我的声音"已克隆完成，可以开始使用。', 1),
    (2, '配音完成', '剧本"广告配音"已合成完成，请前往查看。', 2);

-- ============================================================
-- [B] 边界数据
-- ============================================================
-- 边界：最大长度手机号（20字符）
INSERT INTO `user` (phone, membership_level) VALUES ('12345678901234567890', 0);

-- 边界：最小/最大语速、音量、音调
INSERT INTO tts_record (user_id, voice_id, text, text_length, speed, volume, pitch, audio_url, status) VALUES
    (1, 1, '语速最小测试。', 7, 0.5, 50, 0, '/tts/boundary/speed_min.wav', 1),   -- speed=0.5 (MIN)
    (1, 1, '语速最大测试。', 7, 2.0, 50, 0, '/tts/boundary/speed_max.wav', 1),   -- speed=2.0 (MAX)
    (1, 1, '音量最小测试。', 7, 1.0, 0, 0, '/tts/boundary/volume_min.wav', 1),    -- volume=0 (MIN)
    (1, 1, '音量最大测试。', 7, 1.0, 100, 0, '/tts/boundary/volume_max.wav', 1),  -- volume=100 (MAX)
    (1, 1, '音调最低测试。', 7, 1.0, 50, -12, '/tts/boundary/pitch_min.wav', 1), -- pitch=-12 (MIN)
    (1, 1, '音调最高测试。', 7, 1.0, 50, 12, '/tts/boundary/pitch_max.wav', 1);  -- pitch=+12 (MAX)

-- 边界：超长剧本（含多种字符集）
INSERT INTO script_dub_task (user_id, script_name, script_text, charset, role_count, status) VALUES
    (1, '超长剧本', REPEAT('剧本测试文本内容。', 1000), 'UTF-8', 1, 1);

-- 边界：音色名称最大长度（100字符）
INSERT INTO voice (user_id, voice_name, clone_mode, status, source) VALUES
    (1, LEFT(REPEAT('超长音色名称', 20), 100), 0, 1, 'cloned');

-- 边界：分享标签最大长度（500字符） — 使用测试数据中的超长音色名称（voice_id 相对于种子数据的偏移）
INSERT INTO voice_share (voice_id, user_id, tags, status) VALUES
    (12, 1, LEFT(REPEAT('标签,', 200), 500), 0);

-- 边界：retry_count = 0（默认值）和 retry_count = 127（TINYINT MAX）
INSERT INTO voice (user_id, voice_name, clone_mode, status, source, retry_count) VALUES
    (1, '零次重试', 0, 1, 'cloned', 0),
    (1, '最大重试', 0, 1, 'cloned', 127);

-- ============================================================
-- [A] 异常数据
-- ============================================================
-- 异常：克隆失败
INSERT INTO voice (user_id, voice_name, clone_mode, status, source, error_message, retry_count) VALUES
    (1, '失败的声音', 0, 2, 'cloned', '音频质量不足，信噪比低于20dB', 3);

-- 异常：处理中的音色（需在分享之前创建）
INSERT INTO voice (user_id, voice_name, clone_mode, status, source) VALUES
    (1, '处理中', 0, 0, 'cloned');

-- 异常：已下架的分享（分享处理中的音色然后下架）
INSERT INTO voice_share (voice_id, user_id, status) VALUES
    (16, 1, 0);

-- 异常：TTS 合成失败
INSERT INTO tts_record (user_id, voice_id, text, text_length, status) VALUES
    (1, 1, '', 0, 2);  -- 空文本合成

-- 异常：配音任务失败
INSERT INTO script_dub_task (user_id, script_name, script_text, status, error_message) VALUES
    (1, '失败任务', '无法处理的内容', 2, '角色映射关系无效');

-- 异常：已过期的验证码
INSERT INTO verification_code (phone, code, purpose, expires_at) VALUES
    ('13800138001', '000000', 1, DATE_SUB(NOW(), INTERVAL 1 HOUR));

-- 异常：已使用的验证码
INSERT INTO verification_code (phone, code, purpose, expires_at, used) VALUES
    ('13800138001', '999999', 0, DATE_ADD(NOW(), INTERVAL 5 MINUTE), 1);

-- 异常：处理中的 TTS
INSERT INTO tts_record (user_id, voice_id, text, text_length, status) VALUES
    (1, 1, '正在合成中...', 7, 0);

-- ============================================================
-- 最终数据统计
-- ============================================================
SELECT '[N] 正常测试' AS category, COUNT(*) AS count, 'user' AS tbl FROM user WHERE phone LIKE '138%'
UNION ALL SELECT '[N]', COUNT(*), 'voice' FROM voice WHERE source='cloned' AND voice_name IN ('我的声音','朗读专用','高保真声音')
UNION ALL SELECT '[N]', COUNT(*), 'tts_record' FROM tts_record WHERE text LIKE '%欢迎使用%'
UNION ALL SELECT '[B]', COUNT(*), 'user' FROM user WHERE phone='12345678901234567890'
UNION ALL SELECT '[B]', COUNT(*), 'voice' FROM voice WHERE voice_name IN ('零次重试','最大重试')
UNION ALL SELECT '[A]', COUNT(*), 'voice' FROM voice WHERE status=2
UNION ALL SELECT '[A]', COUNT(*), 'tts_record' FROM tts_record WHERE status=2
UNION ALL SELECT '[A]', COUNT(*), 'verification_code' FROM verification_code WHERE used=1 OR expires_at < NOW()
ORDER BY category;
