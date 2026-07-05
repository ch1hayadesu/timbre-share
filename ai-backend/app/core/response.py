from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.error_code import ErrorCode, ERROR_MESSAGES
from app.core.exceptions import AppException


class ApiResponse:
    @staticmethod
    def success(data: Any = None, message: str = "success") -> JSONResponse:
        return JSONResponse(
            content={
                "code": ErrorCode.SUCCESS,
                "message": message,
                "data": data,
            }
        )

    @staticmethod
    def error(code: int, message: str | None = None, data: Any = None) -> JSONResponse:
        return JSONResponse(
            status_code=_http_status(code),
            content={
                "code": code,
                "message": message or ERROR_MESSAGES.get(code, "未知错误"),
                "data": data,
            },
        )

    @staticmethod
    def paginated(items: list, total: int, page: int, page_size: int) -> JSONResponse:
        return JSONResponse(
            content={
                "code": ErrorCode.SUCCESS,
                "message": "success",
                "data": {
                    "items": items,
                    "pagination": {
                        "page": page,
                        "pageSize": page_size,
                        "total": total,
                        "totalPages": (total + page_size - 1) // page_size,
                    },
                },
            }
        )


def _http_status(code: int) -> int:
    if 20000 <= code < 30000:
        return 401 if code == 20001 else 400
    if 10000 <= code < 20000:
        mapping = {10001: 400, 10002: 404, 10003: 403, 10004: 429, 10006: 503}
        return mapping.get(code, 400)
    return 500


async def app_exception_handler(request: Request, exc: AppException):
    return ApiResponse.error(code=exc.code, message=exc.message, data=exc.data)
