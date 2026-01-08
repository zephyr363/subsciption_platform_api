from fastapi import APIRouter

from .session import session_routes
from .user import user_routes

v1_routes = APIRouter(prefix="/api/v1")

v1_routes.include_router(user_routes)
v1_routes.include_router(session_routes)

__all__ = ["v1_routes"]
