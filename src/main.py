from fastapi import FastAPI
import uvicorn
from src.api import auth
from src.api import get_info
from src.api import write_info


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(get_info.router, prefix="/get_info", tags=["get_info"])
app.include_router(write_info.router, prefix="/write_info", tags=["write_info"])


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload = True)
