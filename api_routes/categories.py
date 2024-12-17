import os
from typing import IO

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

import api_routes.metadata as meta
from api_routes.common import (
    BaseResponse,
    responses_common_200_desc,
    responses_common_post
)
from common.enums import BASE_PATH
from db import crud_categories as crud
from db import database
from schemas.categories import (
    Category,
    CategoryCreate,
    SubCategory,
    SubCategoryCreate
)

router = APIRouter(prefix=meta.api_prefix)
TAG = 'Категории'
CHUNK_SIZE = 1024 * 1024


async def save_file(file_full_path: str, file: IO):
    async with aiofiles.open(file_full_path, mode='wb') as stream:
        while contents := file.read(CHUNK_SIZE):
            await stream.write(contents)
        await stream.flush()


@router.post(
    "/category/create",
    tags=[TAG],
    summary="Создать категорию",
    response_model=Category,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def create_category(
    name: str = Query(...),
    slug: str = Query(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не поддерживаемый формат"
        )

    category = await crud.create_category_slug_name(db, slug, name)

    path = os.path.join(
        BASE_PATH,
        'category',
        str(category.id)
    )
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, image.filename)
    await save_file(path, image.file)

    return BaseResponse(Category).get_typed_response_single_as_model(
        await crud.update_category_file(
            db,
            category.id,
            path
        )
    )


@router.put(
    "/category/edit",
    tags=[TAG],
    summary="Изменить категорию",
    response_model=Category,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def edit_category(
    category_id: int = Query(...),
    name: str = Query(None),
    slug: str = Query(None),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(database.get_db_async),
):
    category = BaseResponse(Category).get_typed_response_single_as_model(
        await crud.get_category(db, category_id)
    )
    path = None
    if image:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не поддерживаемый формат"
            )
        if os.path.exists(category.image):
            os.remove(category.image)

        path = os.path.join(
            BASE_PATH,
            'category',
            str(category.id)
        )

        path = os.path.join(path, image.filename)
        await save_file(path, image.file)

    return BaseResponse(Category).get_typed_response_single_as_model(
        await crud.edit_category(
            db,
            id_category=category_id,
            item=CategoryCreate(
                name=name,
                slug=slug,
                image=path
            )
        )
    )


@router.delete(
    "/category/delete",
    tags=[TAG],
    summary="Удалить категорию",
    response_model=Category,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def delete_category(
    category_id: int = Query(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    category = BaseResponse(Category).get_typed_response_single_as_model(
        await crud.get_category(db, category_id)
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категории с id={category_id} нет"
        )

    if os.path.exists(category.image):
        os.remove(category.image)
    await crud.delete_category(db, category.id)

    return category


@router.post(
    "/subcategory/create",
    tags=[TAG],
    summary="Создать подкатегорию",
    response_model=SubCategory,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def create_subcategory(
    category_id: int = Query(...),
    name: str = Query(...),
    slug: str = Query(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не поддерживаемый формат"
        )

    subcategory = await crud.create_subcategory_slug_name(
        db, slug, name, category_id
    )

    path = os.path.join(
        BASE_PATH,
        'category',
        str(category_id),
        'subcategory',
        str(subcategory.id)
    )
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, image.filename)
    await save_file(path, image.file)

    return BaseResponse(SubCategory).get_typed_response_single_as_model(
        await crud.update_subcategory_file(
            db,
            subcategory.id,
            path
        )
    )


@router.put(
    "/subcategory/edit",
    tags=[TAG],
    summary="Изменить подкатегорию",
    response_model=SubCategory,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def edit_subcategory(
    subcategory_id: int = Query(...),
    name: str = Query(None),
    slug: str = Query(None),
    category_id: int = Query(None),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(database.get_db_async),
):
    subcategory = BaseResponse(SubCategory).get_typed_response_single_as_model(
        await crud.get_subcategory(db, subcategory_id)
    )
    path = None
    if image:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не поддерживаемый формат"
            )
        if os.path.exists(subcategory.image):
            os.remove(subcategory.image)

        path = os.path.join(
            BASE_PATH,
            'category',
            str(category_id),
            'subcategory',
            str(subcategory.id)
        )

        path = os.path.join(path, image.filename)
        await save_file(path, image.file)

    return BaseResponse(SubCategory).get_typed_response_single_as_model(
        await crud.edit_subcategory(
            db,
            id_subcategory=subcategory_id,
            item=SubCategoryCreate(
                name=name,
                slug=slug,
                image=path,
                category_id=category_id
            )
        )
    )


@router.delete(
    "/subcategory/delete",
    tags=[TAG],
    summary="Удалить подкатегорию",
    response_model=SubCategory,
    responses=responses_common_post,
    response_description=responses_common_200_desc,
)
async def delete_subcategory(
    subcategory_id: int = Query(...),
    db: AsyncSession = Depends(database.get_db_async),
):
    subcategory = BaseResponse(SubCategory).get_typed_response_single_as_model(
        await crud.get_subcategory(db, subcategory_id)
    )
    if subcategory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подкатегории с id={subcategory_id} нет"
        )

    if os.path.exists(subcategory.image):
        os.remove(subcategory.image)
    await crud.delete_subcategory(db, subcategory.id)

    return subcategory
