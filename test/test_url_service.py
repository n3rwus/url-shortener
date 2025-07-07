import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from pydantic import HttpUrl

from app.service.url_service import UrlsService
from app.models.models import Urls

@pytest.fixture
def fake_repo():
    return MagicMock()

@pytest.fixture
def url_service(fake_repo):
    return UrlsService(fake_repo)

@pytest.fixture
def test_url():
    return Urls(
        id=uuid4(),
        original_url="https://example.com",
        shortened_url="ABC123",
        created=datetime.now(timezone.utc),
        updated=None,
        valid_until=datetime.now(timezone.utc) + timedelta(days=1),
        clicks=0
    )

def test_shorten_url_calls_create(url_service, fake_repo, test_url):
    fake_repo.create_url.return_value = test_url
    result = url_service.shorten_url(original_url=test_url.original_url, valid_until=test_url.valid_until)
    assert result == test_url
    fake_repo.create_url.assert_called_once()

def test_resolve_url_increments_clicks(url_service, fake_repo, test_url):
    fake_repo.get_by_short.return_value = test_url
    fake_repo.increment_clicks.return_value = test_url

    result = url_service.resolve_url("ABC123")
    assert result == test_url
    fake_repo.get_by_short.assert_called_once_with("ABC123")
    fake_repo.increment_clicks.assert_called_once_with(test_url)

def test_resolve_url_not_found(url_service, fake_repo):
    fake_repo.get_by_short.return_value = None
    result = url_service.resolve_url("NOPE123")
    assert result is None

def test_get_url_by_id(url_service, fake_repo, test_url):
    fake_repo.get_by_id.return_value = test_url
    result = url_service.get_url_by_id(test_url.id)
    assert result == test_url

def test_get_url_by_original(url_service, fake_repo, test_url):
    fake_repo.get_by_original.return_value = test_url
    result = url_service.get_url_by_original(test_url.original_url)
    assert result == test_url

@pytest.mark.asyncio
async def test_get_all_urls_async(url_service, fake_repo, test_url):
    fake_repo.get_all_urls.return_value = [test_url]
    result = await url_service.get_all_urls()
    assert result == [test_url]
    fake_repo.get_all_urls.assert_called_once()

def test_delete_url_success(url_service, fake_repo, test_url):
    fake_repo.get_by_short.return_value = test_url
    fake_repo.delete_url.return_value = True
    result = url_service.delete_url("ABC123")
    assert result is True
    fake_repo.delete_url.assert_called_once_with(test_url)

def test_delete_url_not_found(url_service, fake_repo):
    fake_repo.get_by_short.return_value = None
    result = url_service.delete_url("XXX999")
    assert result is False

def test_is_url_expired_true(url_service, fake_repo, test_url):
    # Expired case
    expired_url = test_url
    expired_url.valid_until = datetime.now(timezone.utc) - timedelta(days=1)
    fake_repo.get_by_short.return_value = expired_url

    result = url_service.is_url_expired("ABC123")
    assert result is True

def test_is_url_expired_false(url_service, fake_repo, test_url):
    fake_repo.get_by_short.return_value = test_url
    result = url_service.is_url_expired("ABC123")
    assert result is False
