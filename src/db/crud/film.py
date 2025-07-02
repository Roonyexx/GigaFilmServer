from sqlalchemy import *
from src.schemas.film_status import FilmStatusSet, FilmStatusRead
from src.models.models import Film, FilmGenres, FilmStatus, Genre
from src.schemas.film import FilmBase
from sqlalchemy.ext.asyncio import async_session
import src.core.security as sec
from sqlalchemy.exc import SQLAlchemyError

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


async def getFilmStatus(db: async_session, user_id: str, film_id:int):
    stmt = select(FilmStatus).where(
        FilmStatus.user_id == user_id,
        FilmStatus.film_id == film_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def upsertFilmStatus(
    db: async_session,
    user_id: str,
    film_id: int,
    status_id: int = None,
    user_score: float = None
):
    existing = await getFilmStatus(db, user_id, film_id)
    action = "updated"
    if existing:
        if status_id is not None:
            existing.status_id = status_id
        if user_score is not None:
            existing.user_score = user_score
    else:
        new_status = FilmStatus(
            user_id=user_id,
            film_id=film_id,
            status_id=status_id,
            user_score=user_score
        )
        db.add(new_status)
        action = "created"
    try:
        await db.commit()
    except SQLAlchemyError as e:
        return {"ok": False, "exception": str(e)}
    return {"ok": True, "action": action}

async def setFilmUserStatus(db: async_session, user_id: str, film_id: int, status_id: int):
    return await upsertFilmStatus(db, user_id, film_id, status_id=status_id)

async def setFilmUserScore(db: async_session, user_id: str, film_id: int, user_score: float):
    return await upsertFilmStatus(db, user_id, film_id, user_score=user_score)


