import pytest
import pytest_asyncio
from app.models.game import Game
from app.models.user import User

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()



@pytest.mark.asyncio
async def test_game_relationships(db_session):
    user_x = User(username="x")
    user_o = User(username="o")

    db_session.add_all([user_x, user_o])
    await db_session.commit()

    game = Game(
        player_x_id=user_x.id,
        player_o_id=user_o.id
    )

    db_session.add(game)
    await db_session.commit()
    await db_session.refresh(game)

    assert game.player_x.username == "x"
    assert game.player_o.username == "o"