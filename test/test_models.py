import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.sql_database import Base
from app.models.models import Urls  # Adjust path to your Urls model


@pytest.fixture
def test_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_url_entry(test_session):
    test_uuid = uuid.uuid4()
    new_url = Urls(
        id=test_uuid,
        original_url="https://example.com",
        shortened_url="exmpl",
        clicks=0,
        valid_until=datetime.now(timezone.utc) + timedelta(days=30)
    )

    test_session.add(new_url)
    test_session.commit()

    result = test_session.query(Urls).filter_by(shortened_url="exmpl").first()
    assert result is not None
    assert result.id == test_uuid
    assert result.original_url == "https://example.com"
    assert result.clicks == 0
    assert result.valid_until is not None
