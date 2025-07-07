import uuid
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Urls(Base):
    __tablename__ = "urls"

    id = Column(uuid.UUID, primary_key=True)
    original_url = Column(String(150), unique=True, nullable=False)
    shortened_url = Column(String(50), unique=True, nullable=False, index=True)
    clicks = Column(Integer, default=0, nullable=False)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now())
    valid_until = Column(DateTime, nullable=True)
