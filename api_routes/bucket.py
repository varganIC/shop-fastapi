from fastapi import (
    APIRouter,
    Body,
    Depends,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession

import api_routes.metadata as meta
from api_routes.common import (
    BaseResponse,
    responses_common_200_desc,
    responses_common_delete,
    responses_common_get,
    responses_common_post
)
from db import crud_bucket as crud
from db import database
from schemas.auth import UserContext
from schemas.bucket import (
    Bucket,
    BucketAdd,
    BucketComposition,
    BucketCreate
)
from service_auth import auth

router = APIRouter(prefix=meta.api_prefix)
TAG = 'Корзина'


@router.post(
    "/bucket/add",
    tags=[TAG],
    summary="Добавить продукт в корзину",
    response_model=Bucket,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def bucket_add(
    item: BucketAdd = Body(...),
    user: UserContext = Depends(auth.get_context_user),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(Bucket).get_typed_response_single_as_model(
        await crud.bucket_add(db, item, user.id)
    )


@router.put(
    "/bucket/edit",
    tags=[TAG],
    summary="Редактировать кол-во продукта в корзине",
    response_model=Bucket,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def bucket_edit(
    item: BucketCreate = Body(...),
    user: UserContext = Depends(auth.get_context_user),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(Bucket).get_typed_response_single_as_model(
        await crud.bucket_edit(db, item, user.id)
    )


@router.delete(
    "/bucket/delete",
    tags=[TAG],
    summary="Удалить продукт из корзины",
    responses=responses_common_delete,
    response_description=responses_common_200_desc,
)
async def bucket_delete(
    product_id: int = Query(...),
    user: UserContext = Depends(auth.get_context_user),
    db: AsyncSession = Depends(database.get_db_async),
):
    await crud.bucket_delete(db, product_id, user.id)

    return BaseResponse.get_no_content_response()


@router.delete(
    "/bucket/clear/all",
    tags=[TAG],
    summary="Очистить корзину",
    responses=responses_common_delete,
    response_description=responses_common_200_desc,
)
async def bucket_clear_all(
    user: UserContext = Depends(auth.get_context_user),
    db: AsyncSession = Depends(database.get_db_async),
):
    await crud.bucket_clear_all(db, user.id)

    return BaseResponse.get_no_content_response()


@router.get(
    "/bucket/composition",
    tags=[TAG],
    summary="Состав корзины",
    response_model=BucketComposition,
    responses=responses_common_get,
    response_description=responses_common_200_desc,
)
async def get_amount_cost(
    user: UserContext = Depends(auth.get_context_user),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(BucketComposition).get_typed_response_single_as_model(
        await crud.get_amount_cost_bucket(db, user.id)
    )
