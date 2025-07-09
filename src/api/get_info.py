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
    return await getUserFilms(session, id)

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