from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str


class UserDB(User):
    hashed_password: str
    id: int


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class UserLogin(User):
    password: str


class UserContext(User):
    id: int


class UserResponse(UserContext):
    token: Token
