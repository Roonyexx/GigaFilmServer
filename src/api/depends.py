from typing import Annotated
from fastapi import Depends
from src.db.database import getSession
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(getSession)]