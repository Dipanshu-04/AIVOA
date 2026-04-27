from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

class Base(DeclarativeBase):
    pass

# We'll default to a local sqlite database for simple development/demo purposes
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./aivoa_crm.db")

# SQLite needs check_same_thread=False, MySQL/Postgres do not
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    FastAPI dependency that provides a database session and ensures it is closed 
    after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---
# Explanation:
# Centralizes database connection setup and exposes the `get_db` dependency for FastAPI routes.
