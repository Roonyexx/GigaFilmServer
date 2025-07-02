
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import UUID


class FilmStatusBase(BaseModel):
    user_token: str
    film_id: int


class FilmStatusSet(FilmStatusBase):
    status_id: int

class FilmScoreSet(FilmStatusBase):
    user_score: float


class FilmStatusRead(FilmStatusBase):
    status_id: int
    user_id: str
    film_id: int
