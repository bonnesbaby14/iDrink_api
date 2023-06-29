from fastapi import FastAPI

from .database import get_db_session
from .routes import login

app = FastAPI()



app.include_router(login.router)
