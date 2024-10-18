from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    hashed_password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
