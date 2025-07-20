from sqlalchemy.orm import Session
from app.db.sql_database import get_db

def test_get_db_yields_session():
    # Manually call the generator
    generator = get_db()
    session = next(generator)

    # Assert it's a SQLAlchemy session
    assert isinstance(session, Session)

    # Close generator and ensure no exceptions raised on cleanup
    try:
        next(generator)
    except StopIteration:
        pass
