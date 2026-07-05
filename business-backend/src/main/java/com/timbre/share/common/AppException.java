package com.timbre.share.common;

import lombok.Getter;

@Getter
public class AppException extends RuntimeException {
    private final int code;

    public AppException(int code, String message) {
        super(message);
        this.code = code;
    }

    public static AppException notFound(String resource) {
        return new AppException(ErrorCode.NOT_FOUND, resource + "不存在");
    }

    public static AppException unauthorized(String message) {
        return new AppException(ErrorCode.UNAUTHORIZED, message);
    }

    public static AppException forbidden() {
        return new AppException(ErrorCode.FORBIDDEN, "无权限操作");
    }

    public static AppException paramError(String message) {
        return new AppException(ErrorCode.PARAM_ERROR, message);
    }
}
