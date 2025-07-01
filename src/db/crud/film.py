from sqlalchemy import *
from src.models.models import Film, FilmGenres, FilmStatus, Genre
from src.schemas.film import FilmBase
from sqlalchemy.ext.asyncio import async_session

from src.schemas.user import UserSchema

async def getFilmGenres(db: async_session, film: FilmBase):
    statement = (
        select(Genre.name, Film.id)
        .join(FilmGenres, Film.id == film.id)
        .join(Genre, FilmGenres.genre_id == Genre.id)
        .where(Film.id == film.id)
    )

    res = await db.execute(statement)
    return res.scalars().all()


async def getUserFilms(db: async_session, userId: str):
    statement = (
        select(FilmStatus)
        .where(FilmStatus.user_id == userId)
    )
    res = await db.execute(statement)

    filmStatuses = res.scalars().all()

    return [
        {
            "film_id": fs.film_id,
            "status_id": fs.status_id,
            "user_score": float(fs.user_score) if fs.user_score is not None else None,
        }
        for fs in filmStatuses
    ]


