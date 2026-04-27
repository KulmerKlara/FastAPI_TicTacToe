import uuid
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None


class UserOut(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True