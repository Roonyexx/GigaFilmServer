from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.schemas.user import UserCreate
from sqlalchemy import text
from sqlalchemy.exc import *


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost/GigaFilm"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



