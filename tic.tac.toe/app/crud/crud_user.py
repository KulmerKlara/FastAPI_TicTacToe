import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDUser:
    async def create(self, db: AsyncSession, *, username: str) -> User:
        user = User(username=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get(self, db: AsyncSession, user_id: uuid.UUID) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()


    async def delete(self, db: AsyncSession, *, user: User) -> None:
        await db.delete(user)
        await db.commit()

user = CRUDUser()