from fastapi import FastAPI
import uvicorn
from api import auth


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    
    uvicorn.run("main:app", reload = True)