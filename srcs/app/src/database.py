from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

with open(os.getenv('DB_PASSWORD_FILE', '/run/secrets/db_password'), 'r') as f:
    DB_PASSWORD = f.read().strip()

DATABASE_URL = f"mysql+pymysql://gamehub_user:{DB_PASSWORD}@mariadb:3306/gamehub"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)