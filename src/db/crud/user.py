from sqlalchemy.ext.asyncio import async_session
from src.models.user import User
from src.schemas.user import *
from passlib.hash import bcrypt

async def createUser(db: async_session, user: UserCreateSchema) -> User:
    hashed_pw = bcrypt.hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_pw)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user