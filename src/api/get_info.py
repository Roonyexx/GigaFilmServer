from fastapi import APIRouter
from src.api.depends import SessionDep, TokenDep
from src.db.crud.film import *
from src.schemas.user import UserWithToken
from src.core import security 


router = APIRouter()


@router.post("/film_genres")
async def filmGenres(film: FilmBase, session: SessionDep):
    return await getFilmGenres(session, film)


@router.post("/user_films")
async def userFilms(session: SessionDep, token: TokenDep):
    id = security.decodeToken(token.credentials)["id"]
    return await getUserFilms(session, id)



    