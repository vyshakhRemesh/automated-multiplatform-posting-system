from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime
from typing import Optional

from app.utils.url_validator import validate_cta_url


class PostingRequest(BaseModel):
    message: str = Field(min_length=1, max_length=200)
    cta_url: HttpUrl

    @field_validator("cta_url")
    @classmethod
    def check_cta_url(cls, value):
        if not validate_cta_url(str(value)):
            raise ValueError("CTA URL must be a valid HTTP or HTTPS URL")

        return value


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[HttpUrl] = None
    public_access: Optional[bool] = None
    datetime: datetime
    error: Optional[str] = None


class PostingResponse(BaseModel):
    results: list[PlatformResult]