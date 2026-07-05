-- ============================================================
-- 音色共享平台 — 数据验证脚本
-- 运行方式: psql -d timbre_share -f 03_verify.sql
-- ============================================================

-- 1. 表结构检查
SELECT '=== 表结构 ===' AS info;
SELECT table_name, table_type, is_insertable_into
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- 2. 字段数量统计
SELECT '=== 各表字段数 ===' AS info;
SELECT
    c.table_name,
    COUNT(*) AS column_count
FROM information_schema.columns c
WHERE c.table_schema = 'public'
GROUP BY c.table_name
ORDER BY c.table_name;

-- 3. 索引检查
SELECT '=== 索引清单 ===' AS info;
SELECT
    tablename AS table_name,
    indexname AS index_name,
    indexdef AS index_definition
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 4. 外键检查
SELECT '=== 外键关系 ===' AS info;
SELECT
    tc.table_name AS child_table,
    kcu.column_name AS child_column,
    ccu.table_name AS parent_table,
    ccu.column_name AS parent_column,
    rc.delete_rule
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
JOIN information_schema.referential_constraints rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name, kcu.column_name;

-- 5. 初始数据量
SELECT '=== 数据量统计 ===' AS info;
SELECT 'user' AS table_name, COUNT(*) AS rows FROM "user"
UNION ALL
SELECT 'voice', COUNT(*) FROM voice
UNION ALL
SELECT 'voice_share', COUNT(*) FROM voice_share
UNION ALL
SELECT 'voice_download', COUNT(*) FROM voice_download
UNION ALL
SELECT 'tts_record', COUNT(*) FROM tts_record
UNION ALL
SELECT 'script_dub_task', COUNT(*) FROM script_dub_task
UNION ALL
SELECT 'verification_code', COUNT(*) FROM verification_code
UNION ALL
SELECT 'notification', COUNT(*) FROM notification
ORDER BY table_name;

-- 6. 预设音色清单
SELECT '=== 预设音色 ===' AS info;
SELECT voice_id, voice_name, clone_mode, source, sample_url
FROM voice
WHERE source = 'preset'
ORDER BY voice_id;

-- 7. 公共区已分享音色
SELECT '=== 公共区分享 ===' AS info;
SELECT vs.share_id, v.voice_name, vs.tags, vs.download_count
FROM voice_share vs
JOIN voice v ON v.voice_id = vs.voice_id
WHERE vs.status = 1
ORDER BY vs.share_id;
