from fastapi import (
    APIRouter,
    Body,
    Depends,
    Path,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession

import api_routes.metadata as meta
from api_routes.common import (
    BaseResponse,
    responses_common_200_desc,
    responses_common_delete,
    responses_common_post
)
from db import crud_products as crud
from db import database
from schemas.products import Product, ProductCreate

router = APIRouter(prefix=meta.api_prefix)
TAG = 'Продукты'


@router.post(
    "/products/create",
    tags=[TAG],
    summary="Создать продукт",
    response_model=Product,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def create_product(
    item: ProductCreate = Body(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(Product).get_typed_response_single_as_model(
        await crud.create_product(db, item)
    )


@router.put(
    "/products/edit/{product_id}",
    tags=[TAG],
    summary="Редактировать продукт",
    response_model=Product,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def edit_product(
    product_id: int = Path(...),
    item: ProductCreate = Body(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(Product).get_typed_response_single_as_model(
        await crud.edit_product(db, product_id, item)
    )


@router.delete(
    "/products/delete",
    tags=[TAG],
    summary="Удалить продукт",
    responses=responses_common_delete,
    response_description=responses_common_200_desc,
)
async def delete_product(
    product_id: int = Query(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    await crud.delete_product(db, product_id)

    return BaseResponse.get_no_content_response()
