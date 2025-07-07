import datetime
import uuid
from sqlmodel import Field, SQLModel

class Urls(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    original_url: str
    shortened_url: str = Field(index=True)
    clicks: int = 0
    created: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    valid_until: datetime.datetime | None = None


# # Alternative model definition if the above doesn't work
# from sqlmodel import Field, SQLModel, Column, String, Integer, DateTime
# import sqlalchemy as sa
#
#
# class Urls(SQLModel, table=True):
#     __tablename__ = "urls"
#
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     original_url: str = Field(sa_column=Column(String, nullable=False))
#     shortened_url: str = Field(sa_column=Column(String, index=True, unique=True, nullable=False))
#     clicks: int = Field(default=0, sa_column=Column(Integer, default=0))
#     created: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
#     updated: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
#     valid_until: Optional[datetime.datetime] = Field(default=None)