from __future__ import annotations
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import UnauthorizedError


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        public_paths = ["/api/v1/user/send-code", "/api/v1/user/login", "/api/v1/share/public", "/api/v1/voice/presets", "/health", "/docs", "/openapi.json"]
        if request.url.path in public_paths:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise UnauthorizedError("请先登录")

        return await call_next(request)
