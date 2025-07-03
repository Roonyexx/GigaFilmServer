from fastapi import APIRouter
from src.api.depends import SessionDep
from src.schemas.user import UserWithToken
import requests


router = APIRouter()

@router.post("/new_film")
async def getFilm(user: UserWithToken, session: SessionDep):

    url = "https://api.kinopoisk.dev/v1.4/movie/random?notNullFields=name&year=2020-2024&rating.imdb=7-10"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "NDP9PHV-2CM4WCW-N8DM92V-FMKG2NX"
    }

    response = requests.get(url, headers=headers)
    print(response.text)
    return response.json()