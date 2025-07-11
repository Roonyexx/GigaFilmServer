from fastapi import APIRouter

from src.api.depends import SessionDep, TokenDep
from src.db.crud.film import *
from src.schemas.film_status import *
import src.core.security as sec


router = APIRouter()

@router.post("/content_status")
async def filmStatus(data: ContentStatusSet, session: SessionDep, token: TokenDep):
    user_id = sec.decodeToken(token.credentials)["id"]
    return await setContentUserStatus(session, user_id, data.content_id, data.status_id, data.content_type) 

@router.post("/content_user_score")
async def filmUserScore(data: ContentScoreSet, session: SessionDep, token: TokenDep):
    user_id = sec.decodeToken(token.credentials)["id"]
    return await setContentUserScore(session, user_id, data.content_id, float(data.user_score), data.content_type)
