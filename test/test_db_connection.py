from sqlalchemy.exc import OperationalError

from app.db.database import get_db


def test_db_connection():
    """Test the database connection using the get_db function."""
    try:
        # Using a session from the get_db generator
        db = next(get_db())  # Get a database session

        # Execute a simple query to check the connection
        result = db.execute("SELECT 1")  # Simple query to check the connection
        if result.scalar() == 1:  # If we get a result of 1, it means the DB is reachable
            print("Database connection successful!")
        else:
            print("Unexpected result from the database.")

    except OperationalError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Closing the session after the test
        db.close()


# Call the test function
if __name__ == "__main__":
    test_db_connection()
