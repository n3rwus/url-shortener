from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.main import settings


SQLALCHEMY_DATABASE_URL = \
    (f"postgresql://{settings.USER}:"
     f"{settings.PASSWORD.get_secret_value()}"
     f"{settings.HOST}:"
     f"{settings.PORT}/"
     f"{settings.DBNAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
