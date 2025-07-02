from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    original_url: HttpUrl  # only valid URLs allowed

class URLInDB(BaseModel):
    original_url: str
    shortened_url: str
    clicks: int
    created: datetime
    updated: datetime
    valid_until: datetime
