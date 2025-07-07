import random
import string
import time
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from app.models.models import Urls


class UrlsRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_short(self, shortened_url: str) -> Optional[Urls]:
        return self.db.query(Urls).filter(Urls.shortened_url == shortened_url).first()

    def get_by_id(self, url_id: uuid.UUID) -> Optional[Urls]:
        statement = select(Urls).where(Urls.id == url_id)
        return self.db.exec(statement).first()

    def get_by_original(self, original_url: str) -> Optional[Urls]:
        statement = select(Urls).where(Urls.original_url == original_url)
        return self.db.exec(statement).first()

    def create_url(self, original_url: str, valid_until: Optional[datetime.datetime] = None) -> Urls:
        shortened_url = self._generate_unique_short()
        url_obj = Urls(
            original_url=original_url,
            shortened_url=shortened_url,
            valid_until=valid_until
        )
        self.db.add(url_obj)
        self.db.commit()
        self.db.refresh(url_obj)
        return url_obj

    def delete_url(self, url_obj: Urls) -> bool:
        try:
            self.db.delete(url_obj)
            self.db.commit()
            return True
        except (SQLAlchemyError, IntegrityError) as e:
            self.db.rollback()
            # Log the error if you have logging set up
            # logger.error(f"Failed to delete URL {url_obj.id}: {e}")
            return False

    def increment_clicks(self, url_obj: Urls) -> Urls:
        url_obj.clicks += 1
        url_obj.updated = datetime.datetime.now(datetime.timezone.utc)
        self.db.commit()
        self.db.refresh(url_obj)
        return url_obj

    def is_url_expired(self, url_obj: Urls) -> bool:
        if url_obj.valid_until is None:
            return False
        return datetime.datetime.now(datetime.timezone.utc) > url_obj.valid_until

    def get_all_urls(self, skip: int = 0, limit: int = 100) -> list[Urls]:
        statement = select(Urls).offset(skip).limit(limit)
        return self.db.exec(statement).all()

    def _generate_unique_short(self, length=6) -> str:
        max_attempts = 10

        for _ in range(max_attempts):
            random_charts = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

            if not self.get_by_short(random_charts):
                return random_charts

        # If we couldn't generate unique in max_attempts, use timestamp + random
        timestamp = str(int(time.time()))[-4:]  # Last 4 digits of timestamp
        random_chars = ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=length - 4
        ))
        return timestamp + random_chars
