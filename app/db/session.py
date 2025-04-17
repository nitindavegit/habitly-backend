from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings
SQLALCHEMY_DATABASE_URL = f"{settings.database_url}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()