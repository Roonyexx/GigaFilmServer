from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase



SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost/GigaFilm"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def getSession():
    async with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass








