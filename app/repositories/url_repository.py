import random
import string
import time
import uuid
import datetime
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from app.core.logging_config import setup_logger
from app.core.config import get_settings
from app.models.models import Urls

logger = setup_logger()
settings = get_settings()

def is_url_expired(url_obj: Urls) -> bool:
    expired = url_obj.valid_until is not None and datetime.datetime.now(datetime.timezone.utc) > url_obj.valid_until
    logger.debug(f"Checked expiration for {url_obj.shortened_url}: Expired={expired}")
    return expired



class UrlsRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_short(self, shortened_url: str) -> Optional[Urls]:
        logger.debug(f"Fetching URL by shortened: {shortened_url}")
        return self.db.query(Urls).filter(
            Urls.shortened_url == shortened_url,
            or_(
                Urls.valid_until == None,
                Urls.valid_until > datetime.datetime.now(datetime.timezone.utc)
            )
        ).first()

    def create_url(self, original_url: str, valid_until: Optional[datetime.datetime] = None) -> Urls:
        logger.info(f"Attempting to create or reuse shortened URL for: {original_url}")

        existing_url = self._get_by_original(original_url)
        if existing_url:
            logger.info(f"Found existing valid URL. Returning with short code: {existing_url.shortened_url}")
            return existing_url

        shortened_url = self._generate_unique_short()
        url_obj = Urls(
            original_url=original_url,
            shortened_url=shortened_url,
            valid_until=valid_until
        )

        try:
            self.db.add(url_obj)
            self.db.commit()
            self.db.refresh(url_obj)
            logger.info(f"Created new shortened URL with code: {shortened_url}")
            return url_obj
        except IntegrityError as e:
            self.db.rollback()
            if 'urls_original_url_key' in str(e.orig):
                logger.warning("URL already exists. Fetching and returning the existing entry.")
                return self._get_by_original(original_url)
            logger.error(f"Failed to create shortened URL: {e}")
            raise

    def increment_clicks(self, url_obj: Urls) -> Urls:
        url_obj.clicks += 1
        url_obj.updated = datetime.datetime.now(datetime.timezone.utc)
        self.db.commit()
        self.db.refresh(url_obj)
        logger.debug(f"Incremented clicks for {url_obj.shortened_url}. Total now: {url_obj.clicks}")
        return url_obj

    def _generate_unique_short(self, length=6) -> str:
        logger.debug("Generating unique shortened URL")
        max_attempts = 10

        for _ in range(max_attempts):
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not self.get_by_short(random_chars):
                logger.debug(f"Generated unique short code: {random_chars}")
                return random_chars

        timestamp = str(int(time.time()))[-4:]
        random_fallback = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 4))
        fallback_code = timestamp + random_fallback
        logger.warning(f"Fallback to timestamp-based code: {fallback_code}")
        return fallback_code

    def _get_by_original(self, original_url: str) -> Optional[Urls]:
        logger.debug(f"Fetching URL by original: {original_url}")
        return self.db.query(Urls).filter(
            Urls.original_url == original_url,
            or_(
                Urls.valid_until == None,
                Urls.valid_until > datetime.datetime.now(datetime.timezone.utc)
            )
        ).first()

