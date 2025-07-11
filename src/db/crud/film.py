from sqlalchemy import *
from sqlalchemy.orm import selectinload, Query
from src.models.models import Film, FilmGenre, FilmStatus, Genre, TV, Actor, TVActor, FilmActor, TVGenre
from src.schemas.film import ContentBase
from sqlalchemy.ext.asyncio import async_session
import src.core.security as sec
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.user import UserSchema

async def getFilmGenre(db: async_session, film: ContentBase):
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
        .where(and_(FilmStatus.user_id == userId, FilmStatus.status_id != 3))
        .order_by(desc(FilmStatus.added_at))
    )
    res = await db.execute(statement)

    filmStatuses = res.scalars().all()

    res = []
    for fs in filmStatuses:
        item = None
        if fs.film_id is not None:
            item = { "content_id": fs.film_id, "content_type": "film" }
        elif fs.tv_id is not None:
            item = { "content_id": fs.tv_id, "content_type": "tv" }
        if item:
            item["user_score"] = fs.user_score if fs.user_score is not None else None
            item["status_id"] = fs.status_id if fs.status_id is not None else None
            res.append(item)
    return res




async def getUserFilmsByRate(db: async_session, userId: str):
    statement = (
        select(FilmStatus)
        .where(FilmStatus.user_id == userId)
    )
    res = await db.execute(statement)

    filmStatuses = res.scalars().all()

    liked = []
    disliked = []
    unrated = []

    for fs in filmStatuses:
        item = None
        if fs.film_id is not None:
            item = (fs.film_id, "film")
        elif fs.tv_id is not None:
            item = (fs.tv_id, "tv")
        if item:
            if fs.status_id == 1:
                liked.append(item)
            elif fs.status_id == 2:
                disliked.append(item)
            elif fs.status_id == 3:
                unrated.append(item)

    return liked, disliked, unrated
    


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
    content_type: str = "film"
):
    if content_type == "film":
        existing = await getFilmStatus(db, user_id, content_id)
        kwargs = {"user_id": user_id, "film_id": content_id}
    elif content_type == "tv":
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
    return await upsertContentStatus(db, user_id, film_id, status_id=status_id, content_type=contentType)

async def setContentUserScore(db: async_session, user_id: str, film_id: int, user_score: float, contentType: str):
    return await upsertContentStatus(db, user_id, film_id, user_score=user_score, content_type=contentType)


async def getFilmAbout(db: async_session, film_id: int):
    statement = select(Film).options(selectinload(Film.genres), selectinload(Film.director)).where(Film.id == film_id)
    res = await db.execute(statement)
    film = res.scalar_one_or_none()
    if not film:
        return None

    genres = [genre.name for genre in film.genres]

    actorStmt = (
        select(Actor.id, Actor.name, Actor.character)
        .select_from(Actor)
        .join(FilmActor, FilmActor.actor_id == Actor.id)
        .where(FilmActor.film_id == film_id)
    )
    actor_res = await db.execute(actorStmt)
    actors = [
        {"id": row[0], "name": row[1], "character": row[2]}
        for row in actor_res.fetchall()
    ]

    filmInfo = {
        "id": film.id,
        "original_title": film.original_title,
        "title": film.title,
        "overview": film.overview,
        "popularity": float(film.popularity) if film.popularity is not None else None,
        "poster_path": film.poster_path,
        "release_date": str(film.release_date) if film.release_date else None,
        "vote_average": float(film.vote_average) if film.vote_average is not None else None,
        "vote_count": film.vote_count,
        "budget": film.budget,
        "revenue": int(film.revenue) if film.revenue is not None else None,
        "runtime": film.runtime,
        "genres": film.genres,
        "actors": actors,
        "director": film.director,
        "content_type": "film"
    }
    return filmInfo

async def getTvAbout(db: async_session, tv_id: int):
    statement = select(TV).options(selectinload(TV.genres)).where(TV.id == tv_id)
    res = await db.execute(statement)
    tv = res.scalar_one_or_none()
    if not tv:
        return None

    #genres = [row[0] for row in genre_res.fetchall()]

    actorStmt = (
        select(Actor.id, Actor.name, Actor.character)
        .select_from(Actor)
        .join(TVActor, TVActor.actor_id == Actor.id)
        .where(TVActor.tv_id == tv_id)
    )
    actor_res = await db.execute(actorStmt)
    actors = [
        {"id": row[0], "name": row[1], "character": row[2]}
        for row in actor_res.fetchall()
    ]

    tvInfo = {
        "id": tv.id,
        "original_name": tv.original_name,
        "name": tv.name,
        "overview": tv.overview,
        "popularity": float(tv.popularity) if tv.popularity is not None else None,
        "poster_path": tv.poster_path,
        "first_air_date": str(tv.first_air_date) if tv.first_air_date else None,
        "last_air_date": str(tv.last_air_date) if tv.last_air_date else None,
        "vote_average": float(tv.vote_average) if tv.vote_average is not None else None,
        "vote_count": tv.vote_count,
        "status": tv.status,
        "number_of_episodes": tv.number_of_episodes,
        "number_of_seasons": tv.number_of_seasons,
        "genres": tv.genres,
        "actors": actors,
        "content_type": "tv"
    }
    return tvInfo

async def getContentAbout(db: async_session, content_id: int, content_type: str):
    return await getTvAbout(db, content_id) if content_type == "tv" else await getFilmAbout(db, content_id)

async def searchMovie(query: str,db: async_session):
    film_stmt = (
        select(Film)
        .options(
            selectinload(Film.genres),
            selectinload(Film.actors)
        )
        .where(
            or_(
                Film.title.ilike(f"%{query}%"),
                Film.original_title.ilike(f"%{query}%")
            )
        )
        .order_by(desc(Film.vote_count))
        .limit(20)
    )
    film_result = await db.execute(film_stmt)
    films = film_result.scalars().all()

    for f in films:
        f.content_type = "film"
    return films


async def searchTV(query: str,db: async_session):
    tv_stmt = (
        select(TV)
        .options(
            selectinload(TV.genres),
            selectinload(TV.actors)
        )
        .where(
            or_(
                TV.name.ilike(f"%{query}%"),
                TV.original_name.ilike(f"%{query}%")
            )
        )
        .order_by(desc(TV.vote_count))
        .limit(20)
    )
    tv_result = await db.execute(tv_stmt)
    tvs = tv_result.scalars().all()

    for t in tvs:
        t.content_type = "tv"
    return tvs