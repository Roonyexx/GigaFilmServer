from fastapi import FastAPI
import uvicorn
from src.core.parse import TMDBParser
from src.api import auth
from src.api import get_info
from src.api import write_info
from src.api import recommend


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(get_info.router, prefix="/get_info", tags=["get_info"])
app.include_router(write_info.router, prefix="/write_info", tags=["write_info"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])


if __name__ == "__main__":
    p = TMDBParser()
    uvicorn.run("src.main:app", 
                reload = True, 
                ssl_keyfile="ssl/key.pem", 
                ssl_certfile="ssl/cert.pem"
            )
