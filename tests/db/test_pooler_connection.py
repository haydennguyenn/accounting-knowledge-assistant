from sqlalchemy import create_engine, text

# Try the pooler URL with the password from .env
pooler_url = "postgresql://postgres.fwxeuxawigqenjfijrrt:zuwZd98sLQC5IIyv@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres"
print(f"Testing pooler URL...")

engine = create_engine(pooler_url, pool_pre_ping=True)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        print(f"✓ Connected successfully! Result: {result}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
