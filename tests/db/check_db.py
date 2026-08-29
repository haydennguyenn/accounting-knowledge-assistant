from app.db.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    print("Connected:", conn.execute(text("SELECT 1")).scalar())