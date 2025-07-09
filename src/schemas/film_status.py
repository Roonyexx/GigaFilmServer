
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import UUID


class ContentStatusBase(BaseModel):
    content_id: int
    content_type: str


class ContentStatusSet(ContentStatusBase):
    status_id: int

class ContentScoreSet(ContentStatusBase):
    user_score: float


class ContentStatusRead(ContentStatusBase):
    status_id: int
    user_id: str
    film_id: int
