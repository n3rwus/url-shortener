import os
import pytest
from app.core.config import get_settings

@pytest.fixture(scope="session", autouse=True)
def set_required_env():
    os.environ["USER"] = "test_user"
    os.environ["PASSWORD"] = "test_pass"
    os.environ["HOST"] = "localhost"
    os.environ["PORT"] = "5432"
    os.environ["DBNAME"] = "test_db"

    get_settings.cache_clear()  # Refresh after setting env vars
