from fastapi import APIRouter

from app.api.routes import games

api_router = APIRouter()
api_router.include_router(games.router, prefix="/games", tags=["games"])
