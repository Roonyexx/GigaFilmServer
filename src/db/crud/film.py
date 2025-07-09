from sqlalchemy import *
from src.models.models import Film, FilmGenre, FilmStatus, Genre
from src.schemas.film import FilmBase
from sqlalchemy.ext.asyncio import async_session
import src.core.security as sec
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.user import UserSchema

async def getFilmGenre(db: async_session, film: FilmBase):
    statement = (
        select(Genre.name, Film.id)
        .join(FilmGenre, Film.id == film.id)
        .join(Genre, FilmGenre.genre_id == Genre.id)
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
            "film_id": fs.film_id if fs.film_id is not None else None,
            "tv_id": fs.tv_id if fs.tv_id is not None else None,
            "status_id": fs.status_id,
            "user_score": float(fs.user_score) if fs.user_score is not None else None
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

async def getTvStatus(db: async_session, user_id: str, tv_id:int):
    stmt = select(FilmStatus).where(
        FilmStatus.user_id == user_id,
        FilmStatus.tv_id == tv_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def upsertContentStatus(
    db: async_session,
    user_id: str,
    content_id: int,
    status_id: int = None,
    user_score: float = None,
    contentType: str = "film"
):
    if contentType == "film":
        existing = await getFilmStatus(db, user_id, content_id)
        kwargs = {"user_id": user_id, "film_id": content_id}
    elif contentType == "tv":
        existing = await getTvStatus(db, user_id, content_id)
        kwargs = {"user_id": user_id, "tv_id": content_id}
    else:
        return {"ok": False, "exception": "Unknown contentType"}

    action = "updated"
    if existing:
        if status_id is not None:
            existing.status_id = status_id
        if user_score is not None:
            existing.user_score = user_score
    else:
        new_status = FilmStatus(
            **kwargs,
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

async def setContentUserStatus(db: async_session, user_id: str, film_id: int, status_id: int, contentType: str):
    return await upsertContentStatus(db, user_id, film_id, status_id=status_id, contentType=contentType)

async def setContentUserScore(db: async_session, user_id: str, film_id: int, user_score: float, contentType: str):
    return await upsertContentStatus(db, user_id, film_id, user_score=user_score, contentType=contentType)


