import datetime
from typing import Optional

from app.models.models import Urls
from app.repositories.url_repository import UrlsRepository


class UrlsService:
    def __init__(self, url_repository: UrlsRepository):
        self.url_repository = url_repository

    def create_shortened_url(self, original_url: str, valid_until: Optional[datetime.datetime] = None) -> Urls:
        return self.url_repository.create_url(original_url=original_url, valid_until=valid_until)