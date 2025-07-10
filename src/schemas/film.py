from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.schemas.genre import GenreRead

from datetime import date

class FilmBase(BaseModel):
    id: int
    score: Decimal

class FilmRead(FilmBase):
    genres: List[GenreRead] = []



class ActorOut(BaseModel):
    id: int
    name: str

class FilmOut(BaseModel):
    id: int
    title: str
    original_title: str
    overview: Optional[str]
    poster_path: Optional[str] = Field(None, alias="poster_path")
    vote_average: float
    vote_count: int
    release_date: date
    budget: int
    revenue: int
    runtime: int
    content_type: str = "film"

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )