from sqlalchemy import create_engine, inspect
from app.config import settings


def test_database_schema():
    """Verify that the database is accessible and contains tables."""

    engine = create_engine(settings.SUPABASE_DB_URL)

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    print("\nDatabase tables:")
    for table in tables:
        print(f"  ✓ {table}")

    assert len(tables) > 0, "No tables found in the database"

    print("✓ Database schema exists")