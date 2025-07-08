from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, ConfigDict, field_validator


class UrlsBase(BaseModel):

    original_url: str = Field(..., description="The original full URL to be shortened")
    shortened_url: str = Field(..., description="The short code or shortened URL slug")

class UrlsCreateRequest(BaseModel):

    original_url: str = Field(..., description="The original full URL to be shortened")
    valid_until: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=5),
        description="Expiration date. Defaults to 5 days from now."
    )

    @field_validator("original_url")
    def validate_url(cls, v):
        parsed = urlparse(v)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("URL must start with http or https.")
        return v

class UrlsResponse(BaseModel):
    id: uuid.UUID
    original_url: str
    shortened_url: str
    created: datetime
    updated: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    clicks: int

    model_config = ConfigDict(from_attributes=True)
