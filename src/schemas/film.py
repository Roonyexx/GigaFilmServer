from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.schemas.genre import GenreRead

from datetime import date

class ContentBase(BaseModel):
    id: int
    content_type: str


class ActorOut(BaseModel):
    id: int
    name: str
    character: Optional[str]

class Director(BaseModel):
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
    director: Optional[Director]
    actors: list[ActorOut]
    genres: list[str]

    model_config = ConfigDict(from_attributes=True)


class TVOut(BaseModel):
    id: int
    name: str
    original_name: str
    overview: Optional[str]
    poster_path: Optional[str]
    vote_average: float
    vote_count: int
    first_air_date: date
    last_air_date: Optional[date]
    status: Optional[str]
    number_of_episodes: int
    number_of_seasons: int
    content_type: str = "tv"
    actors: list[ActorOut]
    genres: list[str]

    model_config = ConfigDict(from_attributes=True)