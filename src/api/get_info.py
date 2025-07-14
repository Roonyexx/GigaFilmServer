import asyncio
from fastapi import APIRouter, HTTPException
from src.db.database import SessionLocal
from fastapi import APIRouter, Query
from src.api.depends import SessionDep, TokenDep
from src.db.crud.film import *
from src.schemas.film import ContentBase
from src.schemas.user import UserWithToken
from src.core import security
from src.core.parse import TMDBParser


router = APIRouter()


@router.post("/film_genres")
async def filmGenres(film: ContentBase, session: SessionDep):
    return await getFilmGenre(session, film)


@router.get("/user_films")
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

@router.get("/search")
async def searchFilms(query: str, session: SessionDep, token: TokenDep):

    id = security.decodeToken(token.credentials)["id"]

    films = await searchMovie(query,session,id)
    tvs = await searchTV(query,session,id)

    combined = sorted(films + tvs, key=lambda item: item.vote_count, reverse=True)
    return combined[:20]

@router.post("/where_to_watch")
async def whereToWatch(data: ContentBase):
    parser = TMDBParser()
    rureq = parser.parse(data.id, data.content_type, "RU")
    usreq = parser.parse(data.id, data.content_type, "US")
    return rureq + usreq