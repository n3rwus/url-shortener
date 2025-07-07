from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field

class UrlsBase(BaseModel):
    original_url: HttpUrl = Field(..., description="The original full URL to be shortened")
    shortened_url: str = Field(..., description="The short code or shortened URL slug")

class UrlsCreateRequest(BaseModel):
    original_url: HttpUrl = Field(..., description="The original full URL to be shortened")
    valid_until: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=5),
        description="Expiration date. Defaults to 5 days from now."
    )

class UrlsResponse(BaseModel):
    id: uuid.UUID
    original_url: HttpUrl
    shortened_url: str
    created_at: datetime
    updated: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    clicks: int

    model_config = {
        "from_attributes": True
    }
