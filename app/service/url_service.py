from typing import Optional, List
from pydantic import HttpUrl
from datetime import datetime
import uuid

from app.repositories.url_repository import UrlsRepository, is_url_expired
from app.models.models import Urls
from app.core.logging_config import setup_logger

logger = setup_logger()

class UrlsService:
    def __init__(self, repository: UrlsRepository):
        self.repository = repository

    def shorten_url(self, original_url: HttpUrl, valid_until: Optional[datetime] = None) -> Urls:
        logger.info(f"Service: Shortening URL: {original_url}")
        return self.repository.create_url(original_url, valid_until)

    def resolve_url(self, shortened_url: str) -> Optional[Urls]:
        logger.debug(f"Service: Resolving shortened URL: {shortened_url}")
        url_obj = self.repository.get_by_short(shortened_url)
        if url_obj:
            logger.info(f"Short URL found. Incrementing clicks for: {shortened_url}")
            return self.repository.increment_clicks(url_obj)
        logger.warning(f"Shortened URL not found or expired: {shortened_url}")
        return None

    def get_url_by_id(self, url_id: uuid.UUID) -> Optional[Urls]:
        logger.debug(f"Service: Fetching URL by ID: {url_id}")
        return self.repository.get_by_id(url_id)

    def get_url_by_original(self, original_url: HttpUrl) -> Optional[Urls]:
        logger.debug(f"Service: Fetching URL by original: {original_url}")
        return self.repository.get_by_original(original_url)

    async def get_all_urls(self, skip: int = 0, limit: int = 100) -> List[Urls]:
        logger.debug(f"Service: Fetching all URLs with skip={skip}, limit={limit}")
        return self.repository.get_all_urls(skip=skip, limit=limit)

    def delete_url(self, shortened_url: str) -> bool:
        logger.info(f"Service: Deleting shortened URL: {shortened_url}")
        url_obj = self.repository.get_by_short(shortened_url)
        if url_obj:
            return self.repository.delete_url(url_obj)
        logger.warning(f"Service: Cannot delete. URL not found: {shortened_url}")
        return False

    def is_url_expired(self, shortened_url: str) -> Optional[bool]:
        logger.debug(f"Service: Checking if shortened URL is expired: {shortened_url}")
        url_obj = self.repository.get_by_short(shortened_url)
        if url_obj:
            return is_url_expired(url_obj)
        return None
