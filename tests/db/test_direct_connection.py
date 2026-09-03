from sqlalchemy import create_engine, text
from app.config import settings


def test_direct_connection():
    """Verify that a direct connection using SUPABASE_DB_URL succeeds."""
    db_url = settings.SUPABASE_DB_URL
    assert db_url, "SUPABASE_DB_URL is missing or not set in configuration"

    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1, f"Expected 1, got {result}"

