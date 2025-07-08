from unittest.mock import MagicMock
from datetime import datetime, timedelta, timezone
from app.service.url_service import UrlsService


def test_shorten_url_calls_repository_create_url():
    mock_repo = MagicMock()
    service = UrlsService(repository=mock_repo)

    original_url = "https://example.com"
    valid_until = datetime.now(timezone.utc) + timedelta(days=1)

    service.shorten_url(original_url, valid_until)

    mock_repo.create_url.assert_called_once_with(original_url, valid_until)


def test_resolve_url_found_calls_increment_clicks():
    mock_repo = MagicMock()
    service = UrlsService(repository=mock_repo)

    fake_url = MagicMock()
    mock_repo.get_by_short.return_value = fake_url
    mock_repo.increment_clicks.return_value = "clicked_url"

    result = service.resolve_url("abc123")

    mock_repo.get_by_short.assert_called_once_with("abc123")
    mock_repo.increment_clicks.assert_called_once_with(fake_url)
    assert result == "clicked_url"


def test_resolve_url_not_found_returns_none():
    mock_repo = MagicMock()
    service = UrlsService(repository=mock_repo)

    mock_repo.get_by_short.return_value = None

    result = service.resolve_url("notfound")

    mock_repo.get_by_short.assert_called_once_with("notfound")
    mock_repo.increment_clicks.assert_not_called()
    assert result is None
