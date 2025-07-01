from fastapi import FastAPI
import uvicorn
from src.api import auth
from src.api import get_info


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(get_info.router, prefix="/get_info", tags=["get_info"])


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload = True)
