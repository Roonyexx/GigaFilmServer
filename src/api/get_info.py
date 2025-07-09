import asyncio
from fastapi import APIRouter
from src.db.database import SessionLocal
from src.api.depends import SessionDep, TokenDep
from src.db.crud.film import *
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



    