from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

# Create Engine
engine = create_engine(settings.DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, bind=engine)

# Database session dependency
@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
