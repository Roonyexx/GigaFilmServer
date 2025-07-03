from fastapi import APIRouter

from src.api.depends import SessionDep, TokenDep
from src.db.crud.film import *
from src.schemas.film_status import *
import src.core.security as sec


router = APIRouter()

@router.post("/film_status")
async def filmStatus(data: FilmStatusSet, session: SessionDep, token: TokenDep):
    print(token.credentials)
    user_id = sec.decodeToken(token.credentials)["id"]
    return await setFilmUserStatus(session, user_id, data.film_id, data.status_id) 

@router.post("/film_user_score")
async def filmUserScore(data: FilmScoreSet, session: SessionDep, token: TokenDep):
    user_id = sec.decodeToken(token.credentials)["id"]
    return await setFilmUserScore(session, user_id, data.film_id, float(data.user_score))
