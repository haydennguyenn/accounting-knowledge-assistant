from sqlalchemy import text
from app.db.database import engine


def test_database_connection():
    """Verify that the database engine can connect and execute a basic query."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1, f"Expected 1 from SELECT 1 query, got {result}"
