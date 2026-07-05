-- ============================================================
-- 音色共享平台 — 初始化数据
-- ============================================================

-- ============================================================
-- 1. 系统管理员（用于拥有预设音色）
-- ============================================================
INSERT INTO "user" (user_id, phone, membership_level)
VALUES (0, '00000000000', 1)
ON CONFLICT (user_id) DO NOTHING;

-- ============================================================
-- 2. 预设音色（内置语音库，source=preset）
-- ============================================================
INSERT INTO voice (voice_id, user_id, voice_name, clone_mode, status, source, sample_url)
VALUES
    (1, 0, '温柔女声',   0, 1, 'preset', '/static/samples/gentle_female.wav'),
    (2, 0, '成熟男声',   0, 1, 'preset', '/static/samples/mature_male.wav'),
    (3, 0, '甜美童声',   0, 1, 'preset', '/static/samples/sweet_child.wav'),
    (4, 0, '磁性男声',   0, 1, 'preset', '/static/samples/magnetic_male.wav'),
    (5, 0, '知性女声',   0, 1, 'preset', '/static/samples/intellectual_female.wav'),
    (6, 0, '新闻播报',   0, 1, 'preset', '/static/samples/news_anchor.wav'),
    (7, 0, '动漫正太',   0, 1, 'preset', '/static/samples/anime_boy.wav'),
    (8, 0, '御姐音',     1, 1, 'preset', '/static/samples/queen_female.wav')
ON CONFLICT (voice_id) DO NOTHING;

SELECT setval('voice_voice_id_seq', 100);
-- 预设音色ID固定1-8，后续用户克隆从100开始

-- ============================================================
-- 3. 预设音色分享到公共区（供新用户体验）
-- ============================================================
INSERT INTO voice_share (share_id, voice_id, user_id, tags)
VALUES
    (1, 1, 0, '女声,温柔,推荐'),
    (2, 2, 0, '男声,成熟,推荐'),
    (3, 3, 0, '童声,可爱'),
    (4, 4, 0, '男声,磁性'),
    (5, 5, 0, '女声,知性'),
    (6, 6, 0, '新闻,正式'),
    (7, 7, 0, '动漫,正太'),
    (8, 8, 0, '女声,御姐')
ON CONFLICT (share_id) DO NOTHING;

SELECT setval('voice_share_share_id_seq', 100);

-- ============================================================
-- 4. 系统通知模板（供新用户注册时推送）
-- ============================================================
INSERT INTO notification (notify_id, user_id, title, content, type)
VALUES (1, 0, '平台使用指南', '欢迎使用音色共享平台！您可以上传音频克隆专属音色，使用TTS合成语音，或上传剧本进行智能配音。', 0)
ON CONFLICT (notify_id) DO NOTHING;

SELECT setval('notification_notify_id_seq', 100);
