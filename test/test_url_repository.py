import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.logging_config import setup_logger
from app.models.models import Base, Urls

logger = setup_logger()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # In-memory SQLite database for fast testing

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db():
    """Fixture to create a new database session for each test."""
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture()
def test_url(db):
    """Fixture to add a test URL to the database."""
    url = Urls(
        id=uuid.uuid4(),
        original_url="https://example.com",
        shortened_url="exmpl",
        clicks=0,
        valid_until=None
    )
    db.add(url)
    db.commit()
    logger.info(f"Added test URL: {url.shortened_url} -> {url.original_url}")
    return url


def test_get_by_short(db, test_url):
    """Test the get_by_short method."""
    logger.info(f"Testing get_by_short for shortened URL: {test_url.shortened_url}")

    url = db.query(Urls).filter(Urls.shortened_url == test_url.shortened_url).first()

    assert url is not None, f"URL with shortened_url {test_url.shortened_url} not found."
    assert url.shortened_url == test_url.shortened_url, f"Expected shortened URL {test_url.shortened_url}, but got {url.shortened_url}"
    assert url.original_url == test_url.original_url, f"Expected original URL {test_url.original_url}, but got {url.original_url}"
    assert url.clicks == 0, f"Expected click count to be 0, but got {url.clicks}"

    logger.info(f"Test passed for shortened URL: {test_url.shortened_url}")


def test_get_non_existent_url(db):
    """Test retrieving a non-existent shortened URL."""
    logger.info("Testing retrieval of non-existent shortened URL: 'nonexistent'")

    url = db.query(Urls).filter(Urls.shortened_url == "nonexistent").first()

    assert url is None, "Expected no result for non-existent shortened URL, but found one."

    logger.info("Test passed for non-existent shortened URL.")
