import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone

from app.models.models import Urls
from app.repositories.url_repository import UrlsRepository, is_url_expired


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def repo(mock_db):
    return UrlsRepository(mock_db)


def test_get_by_short(repo, mock_db):
    fake_url = Urls(shortened_url="abc123", valid_until=None)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = fake_url

    result = repo.get_by_short("abc123")
    assert result == fake_url
    mock_db.query.assert_called_once()


def test_create_url_new(repo, mock_db):
    # No existing URL, first call returns None
    repo._get_by_original = MagicMock(return_value=None)
    repo.get_by_short = MagicMock(return_value=None)
    repo._generate_unique_short = MagicMock(return_value="XYZ999")

    mock_obj = MagicMock(spec=Urls)
    with patch("app.repositories.url_repository.Urls", return_value=mock_obj) as mock_model:
        result = repo.create_url("https://example.com")

    mock_db.add.assert_called_once_with(mock_obj)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_obj)
    assert result == mock_obj


def test_create_url_existing(repo):
    mock_url = MagicMock(spec=Urls)
    repo._get_by_original = MagicMock(return_value=mock_url)

    result = repo.create_url("https://example.com")
    assert result == mock_url
    repo._get_by_original.assert_called_once()


def test_increment_clicks(repo, mock_db):
    url = MagicMock(spec=Urls)
    url.clicks = 5
    url.shortened_url = "abc"

    result = repo.increment_clicks(url)

    assert url.clicks == 6
    assert isinstance(url.updated, datetime)
    assert url.updated.tzinfo == timezone.utc
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(url)
    assert result == url


def test_generate_unique_short(repo):
    repo.get_by_short = MagicMock(side_effect=[True, True, False])
    result = repo._generate_unique_short()
    assert isinstance(result, str)
    assert len(result) == 6


def test_is_url_expired_true():
    url = Urls(valid_until=datetime.now(timezone.utc) - timedelta(days=1))
    assert is_url_expired(url) is True


def test_is_url_expired_false():
    url = Urls(valid_until=datetime.now(timezone.utc) + timedelta(days=1))
    assert is_url_expired(url) is False


def test_is_url_expired_none():
    url = Urls(valid_until=None)
    assert is_url_expired(url) is False
