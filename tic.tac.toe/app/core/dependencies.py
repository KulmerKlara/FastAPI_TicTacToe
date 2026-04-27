from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_api_key_user
from app.db.session import get_db
from app.models.user import User


async def get_current_user(
    api_key_user: str = Depends(get_api_key_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    result = await db.execute(select(User).where(User.username == api_key_user))
    user = result.scalar_one_or_none()
    if user:
        return user

    user = User(username=api_key_user)
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        result = await db.execute(select(User).where(User.username == api_key_user))
        return result.scalar_one()

    await db.refresh(user)
    return user
