# import uuid
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.session import get_db
# from app.schemas.users import UserCreate, UserOut
# from app.services.user_service import user_service

# router = APIRouter()

# @router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
#     try:
#         return await user_service.create_user(db, user_in)
#     except ValueError as e:
#         raise HTTPException(status_code=409, detail=str(e))
    

# @router.get("", response_model=list[UserOut])
# async def list_users(db: AsyncSession = Depends(get_db)):
#     return await user_service.get_users(db)



# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
#     success = await user_service.delete_user(db, user_id)

#     if not success:
#         raise HTTPException(status_code=404, detail="User not found")