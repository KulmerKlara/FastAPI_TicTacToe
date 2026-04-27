from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="TicTacToe API")
    app.include_router(api_router)

    @app.on_event("startup")
    async def _startup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app


app = create_app()
