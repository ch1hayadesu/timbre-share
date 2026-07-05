class ErrorCode:
    # Success
    SUCCESS = 0

    # General (1xxxx)
    PARAM_ERROR = 10001
    NOT_FOUND = 10002
    FORBIDDEN = 10003
    RATE_LIMIT = 10004
    INTERNAL_ERROR = 10005
    SERVICE_UNAVAILABLE = 10006

    # User module (2xxxx)
    UNAUTHORIZED = 20001
    INVALID_PHONE = 20002
    CODE_ERROR = 20003
    TOKEN_EXPIRED = 20004
    TOKEN_INVALID = 20005

    # Voice clone module (3xxxx)
    AUDIO_FORMAT_UNSUPPORTED = 30001
    AUDIO_SIZE_EXCEED = 30002
    AUDIO_TOO_SHORT = 30003
    NO_VOICE_DETECTED = 30004
    CLONE_TRAIN_FAILED = 30005
    CONCURRENT_CLONE_LIMIT = 30006

    # TTS module (4xxxx)
    TTS_TEXT_EMPTY = 40001
    TTS_TEXT_TOO_LONG = 40002
    NO_AVAILABLE_VOICE = 40003
    TTS_SYNTHESIS_FAILED = 40004

    # Script dub module (5xxxx)
    SCRIPT_FORMAT_UNSUPPORTED = 50001
    SCRIPT_SIZE_EXCEED = 50002
    SCRIPT_ROLE_LIMIT = 50003
    SCRIPT_PARSE_FAILED = 50004
    SCRIPT_GENERATE_FAILED = 50005
    USER_VOICE_LIBRARY_EMPTY = 50006

    # Share module (6xxxx)
    SHARE_FAILED = 60001
    DOWNLOAD_FAILED = 60002
    VOICE_TRAINING = 60003
    VOICE_FILE_ERROR = 60004


ERROR_MESSAGES: dict[int, str] = {
    ErrorCode.SUCCESS: "success",
    ErrorCode.PARAM_ERROR: "请求参数错误",
    ErrorCode.NOT_FOUND: "资源不存在",
    ErrorCode.FORBIDDEN: "无权限操作",
    ErrorCode.RATE_LIMIT: "请求频率过高",
    ErrorCode.INTERNAL_ERROR: "服务器内部错误",
    ErrorCode.SERVICE_UNAVAILABLE: "服务暂时不可用",
    ErrorCode.UNAUTHORIZED: "用户未登录",
    ErrorCode.INVALID_PHONE: "手机号格式不正确",
    ErrorCode.CODE_ERROR: "验证码错误或已过期",
    ErrorCode.TOKEN_EXPIRED: "Token已过期",
    ErrorCode.TOKEN_INVALID: "Token无效",
    ErrorCode.AUDIO_FORMAT_UNSUPPORTED: "音频格式不支持",
    ErrorCode.AUDIO_SIZE_EXCEED: "音频文件大小超限",
    ErrorCode.AUDIO_TOO_SHORT: "音频时长不足（<5秒）",
    ErrorCode.NO_VOICE_DETECTED: "未检测到有效人声",
    ErrorCode.CLONE_TRAIN_FAILED: "克隆训练失败",
    ErrorCode.CONCURRENT_CLONE_LIMIT: "并发克隆任务超限",
    ErrorCode.TTS_TEXT_EMPTY: "TTS文本为空",
    ErrorCode.TTS_TEXT_TOO_LONG: "TTS文本超限（>1000字）",
    ErrorCode.NO_AVAILABLE_VOICE: "无可用音色",
    ErrorCode.TTS_SYNTHESIS_FAILED: "TTS合成失败",
    ErrorCode.SCRIPT_FORMAT_UNSUPPORTED: "剧本文件格式不支持",
    ErrorCode.SCRIPT_SIZE_EXCEED: "剧本文件大小超限",
    ErrorCode.SCRIPT_ROLE_LIMIT: "剧本角色数量超限",
    ErrorCode.SCRIPT_PARSE_FAILED: "剧本无法解析",
    ErrorCode.SCRIPT_GENERATE_FAILED: "剧本配音生成失败",
    ErrorCode.USER_VOICE_LIBRARY_EMPTY: "用户语音库为空",
    ErrorCode.SHARE_FAILED: "音色分享失败",
    ErrorCode.DOWNLOAD_FAILED: "音色下载失败",
    ErrorCode.VOICE_TRAINING: "音色正在训练中，无法分享",
    ErrorCode.VOICE_FILE_ERROR: "音色文件异常，无法下载",
}
