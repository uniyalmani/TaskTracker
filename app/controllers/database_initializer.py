from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import AppSettings

settings = AppSettings()
URL = settings.get_db_url()
print(URL, "]]]]]]]]]]]]]]]]]]]")
engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
