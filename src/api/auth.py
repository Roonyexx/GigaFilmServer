from fastapi import APIRouter, Depends
from src.api.depends import SessionDep
from src.schemas.user import UserCreateSchema
from src.db.crud.user import *
from src.db.database import *

router = APIRouter()

@router.post("/register")
async def register(user: UserCreateSchema, session: SessionDep):
    return await createUser(session, user)



