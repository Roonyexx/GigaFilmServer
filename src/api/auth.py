from fastapi import APIRouter, Depends
from src.schemas.user import UserCreate
from src.db.crud.user import *
from src.db.database import *

router = APIRouter()

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db = Depends(getDB)):
    return createUser(db, user)

