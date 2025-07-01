
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import UUID


class FilmStatusBase(BaseModel):
    user_score: Optional[Decimal] = None


class FilmStatusCreate(FilmStatusBase):
    film_id: int
    status_id: int


class FilmStatusRead(FilmStatusBase):
    status_id: int
    id: UUID
    film_id: int
