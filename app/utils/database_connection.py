import psycopg2
from psycopg2 import OperationalError

from app.core.logging_config import setup_logger
from app.utils.singleton_meta import SingletonMeta

logger = setup_logger()

class DatabaseConnection(metaclass=SingletonMeta):

    def __init__(self, user, password, host, port, dbname):
        try:
            self.connection = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                dbname=dbname
            )
            logger.info("Database connection established.")
        except OperationalError as e:
            logger.error("Failed to connect to the database.")
            logger.error(f"Error: {e}")
            self.connection = None

    def get_cursor(self):
        if self.connection:
            return self.connection.cursor()
        else:
            raise Exception("No database connection.")

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("Connection closed.")
        else:
            logger.info("No connection to close.")