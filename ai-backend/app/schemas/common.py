from __future__ import annotations
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 12


class PhoneRequest(BaseModel):
    phone: str


class VerifyCodeRequest(BaseModel):
    phone: str
    code: str
