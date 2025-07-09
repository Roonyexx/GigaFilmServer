import asyncio
from fastapi import APIRouter
from src.api.depends import SessionDep, TokenDep
import src.core.security as sec
import src.db.crud.film as db
from src.recommend.recommend import recomender
from src.db.database import SessionLocal


router = APIRouter()

@router.post("/new_films")
async def getFilm(session: SessionDep, token: TokenDep):
    id = sec.decodeToken(token.credentials)["id"]
    liked, disliked, unrated = await db.getUserFilmsByRate(session, id)
    rec = recomender.recommend(liked, disliked, unrated)

    async def get_content(content):
        async with SessionLocal() as new_session:
            await db.setContentUserStatus(new_session, id, content["content_id"], status_id=3, contentType=content["content_type"])
            return await db.getContentAbout(new_session, content["content_id"], content["content_type"])

    result = await asyncio.gather(*[
        get_content(content) for content in rec
    ])

    return result



