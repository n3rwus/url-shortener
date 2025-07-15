import uuid

from sqlalchemy import Column, Integer, String, DateTime, UUID
from sqlalchemy.sql import func
from app.db.sql_database import Base


class Urls(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String(150), unique=True, nullable=False)
    shortened_url = Column(String(50), unique=True, nullable=False, index=True)
    clicks = Column(Integer, default=0, nullable=False)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
    valid_until = Column(DateTime, nullable=True)
