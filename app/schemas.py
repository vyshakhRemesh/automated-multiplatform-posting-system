from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional


class PostingRequest(BaseModel):
    message: str = Field(min_length=1, max_length=200)
    cta_url: HttpUrl


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[HttpUrl] = None
    public_access: Optional[bool] = None
    datetime: datetime
    error: Optional[str] = None


class PostingResponse(BaseModel):
    results: list[PlatformResult]