import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(override=True)

db_url = os.getenv("SUPABASE_DB_URL")
print(f"Using DB URL: {db_url}")

engine = create_engine(db_url, pool_pre_ping=True)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        print(f"✓ Connected successfully! Result: {result}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
