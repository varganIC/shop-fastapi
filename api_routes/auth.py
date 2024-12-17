from http import HTTPStatus

from fastapi import (
    APIRouter,
    Body,
    Depends
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import api_routes.metadata as meta
from api_routes.common import (
    BaseResponse,
    responses_common_200_desc,
    responses_common_post
)
from db import crud_user, database
from schemas.auth import (
    UserContext,
    UserCreate,
    UserDB,
    UserLogin,
    UserResponse
)
from service_auth import auth as auth_user

router = APIRouter(prefix=meta.api_prefix)
TAG = 'Авторизация'


@router.post(
    "/auth/user/login",
    tags=[TAG],
    summary="Аутентификация пользователя",
    response_model=UserResponse,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def login(
    item: UserLogin = Body(...),
    db: AsyncSession = Depends(database.get_db_async)
):
    user = BaseResponse(UserDB).get_typed_response_single_as_model(
        await crud_user.get_user(db, item.username)
    )
    verify = await auth_user.verify_password(
        user.hashed_password,
        item.password
    )
    if not verify:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={
                "message": "Неверный логин или пароль",
                "status": HTTPStatus.UNAUTHORIZED
            }
        )

    user_context = UserContext(
        id=user.id,
        username=user.username
    )
    token = auth_user.update_token(user_context)

    return UserResponse(
        **user_context.dict(),
        token=token
    )


@router.post(
    "/auth/user/create",
    tags=[TAG],
    summary="Регистрация пользователя",
    response_model=UserResponse,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def register_user(
    item: UserLogin = Body(...),
    db: AsyncSession = Depends(database.get_db_async)
):
    user = BaseResponse(UserDB).get_typed_response_single_as_model(
        await crud_user.get_user(db, item.username)
    )
    if user:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "message": "Такой пользователь уже существует",
                "status": HTTPStatus.INTERNAL_SERVER_ERROR
            }
        )

    hashed_pass = auth_user.get_password_hash(item.password)

    user = BaseResponse(UserContext).get_typed_response_single_as_model(
        await crud_user.create_user(
            db,
            UserCreate(
                username=item.username,
                hashed_password=hashed_pass
            )
        )
    )
    token = auth_user.update_token(user)

    return UserResponse(
        **user.dict(),
        token=token
    )
