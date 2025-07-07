import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
import uuid
from app.db.database import Base
from app.models.models import Urls


# Create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db_session():
    # In-memory SQLite database for unit tests
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    # Create all tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    db_session = Session()

    # Yield the session to be used in tests
    yield db_session

    # Commit any changes and rollback if needed
    if db_session.is_active:
        db_session.rollback()
    db_session.close()
    # Drop the tables after the test
    Base.metadata.drop_all(bind=engine)


# Test 1: Model Instantiation
def test_urls_model_instantiation(db_session):
    """Test that the Urls model can be instantiated correctly."""

    # Create a new Urls instance
    url_instance = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",
        shortened_url="abc123",
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    # Add it to the session and commit to trigger default field population
    db_session.add(url_instance)
    db_session.commit()  # Commit to save the instance and trigger default values for `created` and `updated`

    # Refresh the instance to get the updated values from the database
    db_session.refresh(url_instance)

    assert url_instance.original_url == "https://example.com"
    assert url_instance.shortened_url == "abc123"
    assert isinstance(url_instance.created, datetime)  # Now `created` should be set
    assert isinstance(url_instance.updated, datetime)  # Now `updated` should be set
    assert url_instance.clicks == 0  # Default value for clicks
    assert url_instance.valid_until is not None


def test_urls_model_insertion(db_session):
    """Test that the Urls model can be added to the database."""

    # Create a new Urls instance
    new_url = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",
        shortened_url="abc123",
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    # Add the URL to the session and commit
    db_session.add(new_url)
    db_session.commit()

    # Query the URL back
    queried_url = db_session.query(Urls).filter_by(shortened_url="abc123").first()

    assert queried_url is not None
    assert queried_url.original_url == "https://example.com"
    assert queried_url.shortened_url == "abc123"
    assert queried_url.clicks == 0  # Ensure default clicks value
    assert queried_url.created is not None  # Ensure created field is set
    assert queried_url.updated is not None  # Ensure updated field is set


def test_urls_model_uniqueness(db_session):
    """Test the uniqueness constraints on original_url and shortened_url."""

    # Create a new Urls instance
    url1 = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",
        shortened_url="abc123",
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    url2 = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",  # Same original_url
        shortened_url="def456",  # Different shortened_url
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    db_session.add(url1)
    db_session.commit()

    with pytest.raises(Exception):  # Expecting a database integrity error (due to unique constraint)
        db_session.add(url2)
        db_session.commit()


def test_urls_model_defaults(db_session):
    """Test the default values for columns."""

    # Create a new Urls instance with missing `clicks`, `created`, and `updated` fields
    url = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",
        shortened_url="abc123",
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    db_session.add(url)
    db_session.commit()

    # Query the inserted URL to ensure defaults are set
    queried_url = db_session.query(Urls).filter_by(shortened_url="abc123").first()

    assert queried_url is not None
    assert queried_url.clicks == 0  # Default value for clicks
    assert isinstance(queried_url.created, datetime)  # Ensure created is set
    assert isinstance(queried_url.updated, datetime)  # Ensure updated is set


def test_urls_non_null_constraints(db_session):
    """Test that `original_url` and `shortened_url` cannot be null."""

    # Create a new Urls instance with a missing `original_url`
    url1 = Urls(
        id=uuid.uuid4(),
        original_url=None,  # Should not be allowed
        shortened_url="abc123",
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    # Try to add and commit the URL with None as original_url (should raise an error)
    with pytest.raises(Exception):
        db_session.add(url1)
        db_session.commit()

    # Create a new Urls instance with a missing `shortened_url`
    url2 = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",
        shortened_url=None,  # Should not be allowed
        valid_until=datetime.now(timezone.utc) + timedelta(days=5),
    )

    with pytest.raises(Exception):
        db_session.add(url2)
        db_session.commit()
