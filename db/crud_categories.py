from typing import List, Optional

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.models.categories import Category, Subcategory
from schemas.categories import CategoryCreate, SubCategoryCreate


async def create_category(
    db: AsyncSession,
    item: CategoryCreate
) -> Category:
    db_object = Category(**item.dict())
    db.add(db_object)
    await db.commit()

    return db_object


async def create_category_slug_name(
    db: AsyncSession,
    slug: str,
    name: str,
) -> Category:
    db_object = Category(slug=slug, name=name)
    db.add(db_object)
    await db.commit()

    return db_object


async def update_category_file(
    db: AsyncSession,
    id_category: int,
    path: str
) -> Category:
    category = await get_category(db, id_category)
    if category is not None:
        category.image = path
        db.add(category)
        await db.commit()

    return category


async def get_category(
    db: AsyncSession,
    id_category: int
) -> Category:
    return (
        await db.execute(
            select(Category)
            .filter(Category.id == id_category)
        )
    ).scalars().first()


async def delete_category(
    db: AsyncSession,
    id_category: int
) -> None:
    await db.execute(
        delete(Category)
        .filter(Category.id == id_category)
    )
    await db.commit()


async def edit_category(
    db: AsyncSession,
    id_category: int,
    item: CategoryCreate
) -> Category:
    category = await get_category(db, id_category)

    if category is not None:
        for var, value in item.dict().items():
            setattr(category, var, value) if value is not None else None

        category.modified = True
        db.add(category)
        await db.commit()

    return category


async def create_subcategory_slug_name(
    db: AsyncSession,
    slug: str,
    name: str,
    category_id: int
) -> Subcategory:
    db_object = Subcategory(
        slug=slug,
        name=name,
        category_id=category_id
    )
    db.add(db_object)
    await db.commit()

    return db_object


async def create_subcategory(
    db: AsyncSession,
    item: SubCategoryCreate
) -> Subcategory:
    db_object = Subcategory(**item.dict())
    db.add(db_object)
    await db.commit()

    return db_object


async def update_subcategory_file(
    db: AsyncSession,
    id_subcategory: int,
    path: str
) -> Subcategory:
    subcategory = await get_subcategory(db, id_subcategory)
    if subcategory is not None:
        subcategory.image = path
        db.add(subcategory)
        await db.commit()

    return subcategory


async def get_subcategory(
    db: AsyncSession,
    id_subcategory: int
) -> Subcategory:
    return (
        await db.execute(
            select(Subcategory)
            .filter(Subcategory.id == id_subcategory)
        )
    ).scalars().first()


async def edit_subcategory(
    db: AsyncSession,
    id_subcategory: int,
    item: SubCategoryCreate
) -> Subcategory:
    subcategory = await get_subcategory(db, id_subcategory)

    if subcategory is not None:
        for var, value in item.dict().items():
            setattr(subcategory, var, value) if value is not None else None

        subcategory.modified = True
        db.add(subcategory)
        await db.commit()

    return subcategory


async def delete_subcategory(
    db: AsyncSession,
    id_subcategory: int
) -> None:
    await db.execute(
        delete(Subcategory)
        .filter(Subcategory.id == id_subcategory)
    )
    await db.commit()


async def get_all_categories(
    db: AsyncSession,
    take: Optional[int],
    skip: Optional[int]
) -> List[Category]:
    query = (
        await db.execute(
            select(
                Category
            )
            .options(
                selectinload(Category.subcategories)
            )
            .offset(skip)
            .limit(take)
        )
    ).scalars().all()

    return query
