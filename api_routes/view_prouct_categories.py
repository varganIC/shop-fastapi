from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession

import api_routes.metadata as meta
from api_routes.common import (
    BaseResponse,
    responses_common_200_desc,
    responses_common_get
)
from db import (
    crud_categories,
    crud_products,
    database
)
from schemas.categories import CategoryComposite
from schemas.products import ProductComposite

router = APIRouter(prefix=meta.api_prefix)
TAG_PRODUCT = 'Продукты'
TAG_CATEGORY = 'Категории'


@router.get(
    "/products/all",
    tags=[TAG_PRODUCT],
    summary="Получить все продукты в привязке к категориям",
    response_model=List[ProductComposite],
    responses=responses_common_get,
    response_description=responses_common_200_desc,
)
async def get_products_all(
    take: Optional[int] = Query(None),
    skip: Optional[int] = Query(None),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(ProductComposite).get_typed_response_multi_as_model(
        await crud_products.get_all_products(db, take, skip)
    )


@router.get(
    "/category/all",
    tags=[TAG_CATEGORY],
    summary="Получить все категории с подкатегориями",
    response_model=List[CategoryComposite],
    responses=responses_common_get,
    response_description=responses_common_200_desc,
)
async def get_all_categories(
    take: Optional[int] = Query(None),
    skip: Optional[int] = Query(None),
    db: AsyncSession = Depends(database.get_db_async),
):
    return BaseResponse(CategoryComposite).get_typed_response_multi_as_model(
        await crud_categories.get_all_categories(db, take, skip)
    )
