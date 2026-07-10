from __future__ import annotations
from app.core.error_code import ERROR_MESSAGES


class AppException(Exception):
    def __init__(self, code: int, message: str | None = None, data=None):
        self.code = code
        self.message = message or ERROR_MESSAGES.get(code, "未知错误")
        self.data = data


class NotFoundError(AppException):
    def __init__(self, resource: str = "资源"):
        super().__init__(code=10002, message=f"{resource}不存在")


class UnauthorizedError(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(code=20001, message=message or "用户未登录")


class ForbiddenError(AppException):
    def __init__(self, message: str = "无权限操作"):
        super().__init__(code=10003, message=message)


class ParamError(AppException):
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(code=10001, message=message)
