from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.models import Base

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    # Ensure newly added columns exist in sqlite tables
    if "sqlite" in settings.DATABASE_URL:
        import sqlite3
        conn = sqlite3.connect(settings.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check reports table
        cursor.execute("PRAGMA table_info(reports)")
        cols_reports = [r[1] for r in cursor.fetchall()]
        for col, col_type in [
            ("meter_number", "VARCHAR(50)"),
            ("disco_name", "VARCHAR(100)"),
            ("feeder_name", "VARCHAR(150)"),
            ("tariff_band", "VARCHAR(50)"),
            ("hours_supplied", "VARCHAR(50)")
        ]:
            if col not in cols_reports:
                try:
                    cursor.execute(f"ALTER TABLE reports ADD COLUMN {col} {col_type}")
                except Exception:
                    pass
                    
        # Check trending_facts table
        cursor.execute("PRAGMA table_info(trending_facts)")
        cols_facts = [r[1] for r in cursor.fetchall()]
        for col, col_type in [
            ("feeder_name", "VARCHAR(150)"),
            ("disco_name", "VARCHAR(100)"),
            ("tariff_band", "VARCHAR(50)"),
            ("promised_hours", "VARCHAR(50)"),
            ("actual_hours_avg", "VARCHAR(50)"),
            ("overbilling_differential", "VARCHAR(100)"),
            ("docket_ready", "BOOLEAN DEFAULT 0"),
            ("docket_number", "VARCHAR(100)")
        ]:
            if col not in cols_facts:
                try:
                    cursor.execute(f"ALTER TABLE trending_facts ADD COLUMN {col} {col_type}")
                except Exception:
                    pass
        conn.commit()
        conn.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
