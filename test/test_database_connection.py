import pytest
from unittest.mock import patch, MagicMock
from psycopg2 import OperationalError

from app.utils.database_connection import DatabaseConnection


@pytest.fixture
def db_config():
    return {
        "user": "user",
        "password": "pass",
        "host": "localhost",
        "port": "5432",
        "dbname": "testdb"
    }


def test_successful_connection(db_config):
    mock_connection = MagicMock()
    mock_connection.close = MagicMock()

    with patch("app.utils.database_connection.psycopg2.connect", return_value=mock_connection):
        db = DatabaseConnection(**db_config)
        assert db.connection is mock_connection

        cursor = db.get_cursor()
        mock_connection.cursor.assert_called_once()
        assert cursor == mock_connection.cursor.return_value


def test_close_without_connection_logs(db_config):
    with patch("app.utils.database_connection.psycopg2.connect", side_effect=OperationalError("fail")):
        db = DatabaseConnection(**db_config)
        # Should not raise any exception when closing without a connection
        db.close()


def test_singleton_behavior(db_config):
    mock_connection = MagicMock()
    mock_connection.close = MagicMock()

    with patch("app.utils.database_connection.psycopg2.connect", return_value=mock_connection):
        db1 = DatabaseConnection(**db_config)
        db2 = DatabaseConnection(**db_config)
        assert db1 is db2

