import asyncio
from fastapi import APIRouter
from src.db.database import SessionLocal
from fastapi import APIRouter, Query
from src.api.depends import SessionDep, TokenDep
from src.db.crud.film import *
from src.schemas.film import FilmOut
from src.schemas.user import UserWithToken
from src.core import security 


router = APIRouter()


@router.post("/film_genres")
async def filmGenres(film: FilmBase, session: SessionDep):
    return await getFilmGenre(session, film)


@router.post("/user_films")
async def userFilms(session: SessionDep, token: TokenDep):
    id = security.decodeToken(token.credentials)["id"]
    filmsList = await getUserFilms(session, id)

    async def get_content(user_content):
        async with SessionLocal() as new_session:
            content_data = await getContentAbout(new_session, user_content["content_id"], user_content["content_type"])
            return {**user_content, **content_data}


    result = await asyncio.gather(*[
        get_content(content) for content in filmsList
    ])

    return result

@router.get("/search", response_model=list[FilmOut])
async def searchFilms(query: str = Query(..., min_length=1), session: SessionDep = None):
    stmt = (
        select(Film)
        .where(
            or_(
                Film.title.ilike(f"%{query}%"),
                Film.original_title.ilike(f"%{query}%")
            )
        )
        .order_by(desc(Film.vote_count))
        .limit(20)
    )
    result = await session.execute(stmt)
    films = result.scalars().all()
    return films