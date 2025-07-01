from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel

from src.schemas.genre import GenreRead


class FilmBase(BaseModel):
    id: int
    score: Decimal


class FilmRead(FilmBase):
    genres: List[GenreRead] = []
