import re
from datetime import datetime as DateTime
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
from typing import Optional

from app.utils.url_validator import validate_cta_url


class PostingRequest(BaseModel):
    message: str = Field(min_length=1, max_length=200)

    @model_validator(mode="after")
    def validate_message(self):
        urls = re.findall(
            r"https?://[^\s<>\"']+",
            self.message
        )

        if len(urls) != 1:
            raise ValueError(
                "Message must contain exactly one CTA URL"
            )

        if not validate_cta_url(urls[0]):
            raise ValueError("Invalid CTA URL")

        return self

    @property
    def cta_url(self):
        return re.findall(
            r"https?://[^\s<>\"']+",
            self.message
        )[0]



class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[HttpUrl] = None
    public_access: Optional[bool] = None
    datetime: Optional[DateTime] = None
    error: Optional[str] = None



class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]