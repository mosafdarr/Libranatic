from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings

# Create Engine
engine = create_engine(settings.DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, bind=engine)

# Database session dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()