from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql://{settings.USER}:"
    f"{settings.PASSWORD.get_secret_value()}@"
    f"{settings.HOST}:"
    f"{settings.PORT}/"
    f"{settings.DBNAME}"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency function to get a database session.

    Yields:
        SQLAlchemy session: Database session to execute queries

    Notes:
        Session is closed automatically after request is complete
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()