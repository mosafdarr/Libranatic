from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings

# Create Engine
engine = create_engine("postgresql://postgres:mosafdar%%40123@localhost:5432/integrationdb")

# Create Session
SessionLocal = sessionmaker(autocommit=False, bind=engine)

# Database session dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()