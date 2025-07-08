import pytest
import uuid
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
from app.schemas.schema import UrlsCreateRequest, UrlsResponse


def test_urls_create_request_valid_url():
    obj = UrlsCreateRequest(original_url="https://example.com")
    assert obj.original_url == "https://example.com"
    assert isinstance(obj.valid_until, datetime)
    assert obj.valid_until > datetime.now(timezone.utc)


def test_urls_create_request_invalid_url_scheme():
    from pydantic import ValidationError
    with pytest.raises(ValidationError) as exc_info:
        UrlsCreateRequest(original_url="ftp://example.com")
    errors = exc_info.value.errors()

    assert errors[0]["type"] == "value_error"
    assert errors[0]["loc"] == ("original_url",)
    assert "http or https" in errors[0]["msg"]


def test_urls_create_request_default_valid_until():
    req = UrlsCreateRequest(original_url="http://test.com")
    expected = datetime.now(timezone.utc) + timedelta(days=5)
    delta = req.valid_until - expected
    assert abs(delta.total_seconds()) < 2  # allow a small margin for timing


def test_urls_response_from_attributes():
    now = datetime.now(timezone.utc)
    test_id = uuid.uuid4()

    # Simulate ORM-like object
    class FakeUrl:
        def __init__(self):
            self.id = test_id
            self.original_url = "http://example.com"
            self.shortened_url = "abc123"
            self.created = now
            self.updated = now
            self.valid_until = now + timedelta(days=1)
            self.clicks = 42

    response = UrlsResponse.model_validate(FakeUrl())

    assert response.id == test_id
    assert response.original_url == "http://example.com"
    assert response.shortened_url == "abc123"
    assert response.created == now
    assert response.updated == now
    assert response.valid_until == now + timedelta(days=1)
    assert response.clicks == 42
