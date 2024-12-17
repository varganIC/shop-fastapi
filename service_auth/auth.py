from datetime import (
    datetime,
    timedelta,
    timezone
)
from http import HTTPStatus
from typing import Union

import jwt
from fastapi import (
    Depends,
    Header,
    HTTPException
)
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from api_routes.common import BaseResponse
from db import crud_user, database
from schemas.auth import (
    Token,
    UserContext,
    UserDB
)
from settings.settings_loader import token_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(db: AsyncSession, username: str) -> UserDB:
    return (
        BaseResponse(UserDB)
        .get_typed_response_single_as_model(
            await crud_user.get_user(db, username)
        )
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(
    hashed_password: str,
    password: str
) -> bool:
    verify = pwd_context.verify(password, hashed_password)
    if not verify:
        return False
    return True


def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        token_settings.secret_key,
        algorithm=token_settings.algorithm
    )
    return encoded_jwt


def update_token(user: UserContext) -> Token:
    access_token_expires = timedelta(minutes=token_settings.access_exp_minutes)
    access_token = create_access_token(
        data=user.dict(),
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


async def verify_token(
    token: str = Header(...),
    db: AsyncSession = Depends(database.get_db_async)
):
    user_context = get_context_user(token)

    user = await get_user(db, user_context.username)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Неверный или просроченный токен доступа"
        )

    return True


def get_context_user(
    token: str = Header(...),
):
    try:
        payload = jwt.decode(
            token,
            token_settings.secret_key,
            algorithms=[token_settings.algorithm]
        )
        user_context = UserContext(**payload)

        if user_context.username is None:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Неверный или просроченный токен доступа"
            )

    except InvalidTokenError:
        raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Неверный или просроченный токен доступа"
            )

    return user_context
