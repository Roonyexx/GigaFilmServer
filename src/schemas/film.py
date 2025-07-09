from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.schemas.genre import GenreRead


class FilmBase(BaseModel):
    id: int
    score: Decimal

class FilmRead(FilmBase):
    genres: List[GenreRead] = []



class FilmOut(BaseModel):
    id: int
    title: str
    description: str = Field(..., alias="overview")
    imageUrl: str = Field(..., alias="poster_path")
    type: str = "movie"

    model_config = ConfigDict(from_attributes=True)