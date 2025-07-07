import datetime

from pydantic import BaseModel, HttpUrl, Field


class UrlsBase(BaseModel):
    original_url: HttpUrl = Field(..., description="User's HTTP/HTTPS link")

class ShortenUrlRequest(UrlsBase):
    shortened_url: HttpUrl


class UrlsResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        form_attributes = True
