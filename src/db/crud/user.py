from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import exc
from src.models.models import *
from src.schemas.user import *
from passlib.hash import bcrypt


def getHash(password: str):
    return bcrypt.hash(password)

async def createUser(db: async_session, user: UserCreateSchema):
    hashed_pw = getHash(user.password)
    db_user = User(username=user.username, password_hash=hashed_pw)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return {"ok": True}
    
    except exc.IntegrityError as e:
        await db.rollback()
        return {"ok": False, "exception": "Пользователь с таким именем уже существует"}
    

async def loginUser(db: async_session, user: userLogin) -> User | None:
    statement = select(User).where(User.username == user.username)
    res = await db.execute(statement)
    dbUser = res.scalar_one_or_none()
    if dbUser and bcrypt.verify(user.password, dbUser.password_hash):
        return dbUser
    return None
