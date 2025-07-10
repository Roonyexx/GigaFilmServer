from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.schemas.genre import GenreRead


class ContentBase(BaseModel):
    id: int
    content_type: str


class FilmOut(BaseModel):
    id: int
    title: str
    description: str = Field(..., alias="overview")
    imageUrl: str = Field(..., alias="poster_path")
    type: str = "movie"

    model_config = ConfigDict(from_attributes=True)