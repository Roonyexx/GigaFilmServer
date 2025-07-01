from fastapi import APIRouter, Depends
from src.api.depends import SessionDep
from src.schemas.user import UserCreateSchema
from src.db.crud.user import *
from src.db.database import *
from src.core import security

router = APIRouter()

@router.post("/register")
async def register(user: UserCreateSchema, session: SessionDep):
    return await createUser(session, user)


@router.post("/login")
async def login(user: userLogin, session: SessionDep):
    dbUser = await loginUser(session, user)
    if dbUser == None:
        return {"ok": False, "exception": "Неверный логин или пароль"}
    
    token = security.createAccessToken({"username": dbUser.username, "id": str(dbUser.id)})
    return {"ok": True, "access_token": token}


    




