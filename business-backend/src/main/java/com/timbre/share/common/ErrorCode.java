package com.timbre.share.common;

public interface ErrorCode {
    int SUCCESS = 0;

    // General (1xxxx)
    int PARAM_ERROR = 10001;
    int NOT_FOUND = 10002;
    int FORBIDDEN = 10003;
    int RATE_LIMIT = 10004;
    int INTERNAL_ERROR = 10005;
    int SERVICE_UNAVAILABLE = 10006;

    // User (2xxxx)
    int UNAUTHORIZED = 20001;
    int INVALID_PHONE = 20002;
    int CODE_ERROR = 20003;
    int TOKEN_EXPIRED = 20004;
    int TOKEN_INVALID = 20005;

    // Voice clone (3xxxx)
    int AUDIO_FORMAT_UNSUPPORTED = 30001;
    int AUDIO_SIZE_EXCEED = 30002;
    int AUDIO_TOO_SHORT = 30003;
    int NO_VOICE_DETECTED = 30004;
    int CLONE_TRAIN_FAILED = 30005;
    int CONCURRENT_CLONE_LIMIT = 30006;

    // TTS (4xxxx)
    int TTS_TEXT_EMPTY = 40001;
    int TTS_TEXT_TOO_LONG = 40002;
    int NO_AVAILABLE_VOICE = 40003;
    int TTS_SYNTHESIS_FAILED = 40004;

    // Script dub (5xxxx)
    int SCRIPT_FORMAT_UNSUPPORTED = 50001;
    int SCRIPT_SIZE_EXCEED = 50002;
    int SCRIPT_ROLE_LIMIT = 50003;
    int SCRIPT_PARSE_FAILED = 50004;
    int SCRIPT_GENERATE_FAILED = 50005;
    int USER_VOICE_LIBRARY_EMPTY = 50006;

    // Share (6xxxx)
    int SHARE_FAILED = 60001;
    int DOWNLOAD_FAILED = 60002;
    int VOICE_TRAINING = 60003;
    int VOICE_FILE_ERROR = 60004;
}
