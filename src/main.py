from fastapi import FastAPI
import uvicorn
from src.api import auth
from src.api import get_info
from src.api import write_info
from src.api import recomend


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(get_info.router, prefix="/get_info", tags=["get_info"])
app.include_router(write_info.router, prefix="/write_info", tags=["write_info"])
app.include_router(recomend.router, prefix="/recomend", tags=["recomend"])


if __name__ == "__main__":
    uvicorn.run("src.main:app", 
                reload = True, 
                ssl_keyfile="ssl/key.pem", 
                ssl_certfile="ssl/cert.pem"
            )
