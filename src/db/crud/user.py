from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate
from passlib.hash import bcrypt

def createUser(db: Session, user: UserCreate):
    hashed_pw = bcrypt.hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user