from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.presentation.http.v1 import v1_routes

app = FastAPI()


app.include_router(v1_routes)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.auth.secret_key,
    session_cookie=settings.auth.cookie_name,
    max_age=settings.auth.cookie_max_age,
    https_only=settings.auth.httponly,
)
