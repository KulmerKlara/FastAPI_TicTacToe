import pytest

from app.db.session import get_db


@pytest.mark.asyncio
async def test_get_db_returns_session():
    gen = get_db()

    session = await gen.__anext__()

    assert session is not None

    await session.close()