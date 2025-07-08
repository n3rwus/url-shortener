from typing import Optional, List
from datetime import datetime
import uuid

from app.repositories.url_repository import UrlsRepository, is_url_expired
from app.models.models import Urls
from app.core.logging_config import setup_logger

logger = setup_logger()

class UrlsService:
    def __init__(self, repository: UrlsRepository):
        self.repository = repository

    def shorten_url(self, original_url: str, valid_until: Optional[datetime] = None) -> Urls:
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
