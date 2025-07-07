from sqlmodel import Session, create_engine
from app.core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql://{settings.USER}:"
    f"{settings.PASSWORD.get_secret_value()}@"
    f"{settings.HOST}:"
    f"{settings.PORT}/"
    f"{settings.DBNAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def get_db():
    with Session(engine) as session:
        yield session