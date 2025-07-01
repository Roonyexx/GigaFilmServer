from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class GenreBase(BaseModel):
    id: int
    name: str


class GenreRead(GenreBase):
    pass