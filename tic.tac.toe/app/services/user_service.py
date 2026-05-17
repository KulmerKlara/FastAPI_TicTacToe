# import uuid
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.crud.crud_user import user_crud
# from app.models.user import User
# from app.schemas.users import UserCreate


# class UserService:

#     async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
#         existing = await user_crud.get_by_username(db, user_in.username)
#         if existing:
#             raise ValueError("Username already exists")

#         return await user_crud.create(db, username=user_in.username)
    
#     async def get_users(self, db: AsyncSession) -> list[User]:
#         result = await db.execute(select(User))
#         return result.scalars().all()

#     async def delete_user(self, db: AsyncSession, user_id: uuid.UUID) -> bool:
#         user = await user_crud.get(db, user_id)
#         if not user:
#             return False

#         await user_crud.delete(db, user=user)
#         return True


#     user_service = UserService()    