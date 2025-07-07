import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from pydantic import HttpUrl

from app.repositories.url_repository import UrlsRepository
from app.models.models import Urls

@pytest.fixture
def fake_db():
    return MagicMock()

@pytest.fixture
def repository(fake_db):
    return UrlsRepository(fake_db)

@pytest.fixture
def example_url():
    return Urls(
        id=uuid4(),
        original_url="https://example.com",
        shortened_url="ABC123",
        created=datetime.now(timezone.utc),
        updated=None,
        valid_until=datetime.now(timezone.utc) + timedelta(days=1),
        clicks=0
    )

def test_get_by_short(repository, fake_db, example_url):
    fake_db.query().filter().first.return_value = example_url
    result = repository.get_by_short("ABC123")
    assert result == example_url
    fake_db.query().filter.assert_called()

def test_get_by_id(repository, fake_db, example_url):
    fake_db.query().filter().first.return_value = example_url
    result = repository.get_by_id(example_url.id)
    assert result == example_url

def test_get_by_original(repository, fake_db, example_url):
    fake_db.query().filter().first.return_value = example_url
    result = repository.get_by_original(example_url.original_url)
    assert result == example_url

def test_create_url_new(repository, fake_db, example_url):
    # Mock path when URL does not already exist
    repository.get_by_original = MagicMock(return_value=None)
    repository._generate_unique_short = MagicMock(return_value="XYZ789")

    fake_db.add = MagicMock()
    fake_db.commit = MagicMock()
    fake_db.refresh = MagicMock()

    result = repository.create_url(example_url.original_url)
    assert result.shortened_url == "XYZ789"
    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()

def test_create_url_existing_valid(repository, fake_db, example_url):
    repository.get_by_original = MagicMock(return_value=example_url)
    result = repository.create_url(example_url.original_url)
    assert result == example_url

def test_increment_clicks(repository, fake_db, example_url):
    old_clicks = example_url.clicks
    result = repository.increment_clicks(example_url)
    assert result.clicks == old_clicks + 1
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()

def test_delete_url_success(repository, fake_db, example_url):
    result = repository.delete_url(example_url)
    assert result is True
    fake_db.delete.assert_called_once()
    fake_db.commit.assert_called_once()

def test_get_all_urls(repository, fake_db):
    urls = [MagicMock(), MagicMock()]
    fake_db.query().offset().limit().all.return_value = urls
    result = repository.get_all_urls()
    assert result == urls
