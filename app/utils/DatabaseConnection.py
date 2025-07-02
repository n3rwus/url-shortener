import psycopg2
from psycopg2 import OperationalError

from app.utils.SingletonMeta import SingletonMeta


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
            print("Database connection established.")
        except OperationalError as e:
            print("Failed to connect to the database.")
            print(f"Error: {e}")
            self.connection = None

    def get_cursor(self):
        if self.connection:
            return self.connection.cursor()
        else:
            raise Exception("No database connection.")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
        else:
            print("No connection to close.")