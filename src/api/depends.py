from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.db.database import getSession
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(getSession)]
oauth2 = HTTPBearer()
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(oauth2)]