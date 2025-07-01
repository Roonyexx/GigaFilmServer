from fastapi import FastAPI
import uvicorn
from src.api import auth


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload = True)
