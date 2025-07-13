import asyncio
from fastapi import APIRouter
from src.api.depends import SessionDep, TokenDep
import src.core.security as sec
import src.db.crud.film as db
from src.db.crud.film import get_top_10
from src.recommend.recommend import recomender
from src.db.database import SessionLocal

router = APIRouter()

@router.post("/new_films")
async def newFilms(session: SessionDep, token: TokenDep):
    async def get_content(content):
        async with SessionLocal() as new_session:
            await db.setContentUserStatus(new_session, id, content[0], status_id=3,contentType=content[1])
            return await db.getContentAbout(new_session, content[0], content[1])

    id = sec.decodeToken(token.credentials)["id"]
    liked, disliked, unrated = await db.getUserFilmsByRate(session, id)

    if len(unrated) > 5:
        rec = unrated
    elif not liked and not disliked:
        rec = await get_top_10(session)
    else:
        rec = recomender.recommend(liked, disliked, unrated)

    result = await asyncio.gather(*[
        get_content(content) for content in rec
    ])
    return result