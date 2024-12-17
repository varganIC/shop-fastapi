from typing import Optional

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.categories import Category, Subcategory
from db.models.products import Product
from schemas.products import ProductCreate


async def get_all_products(
    db: AsyncSession,
    take: Optional[int],
    skip: Optional[int]
):
    query = (
        await db.execute(
            select(
                Product.id,
                Product.name,
                Product.slug,
                Product.price,
                Product.image_large,
                Product.image_medium,
                Product.image_small,
                Subcategory.name.label("subcategory"),
                Category.name.label("category"),
            )
            .join(
                Subcategory,
                Product.subcategory_id == Subcategory.id
            )
            .join(
                Category,
                Subcategory.category_id == Category.id
            )
            .offset(skip)
            .limit(take)
        )
    ).all()

    return query


async def create_product(
    db: AsyncSession,
    item: ProductCreate
) -> Product:
    db_object = Product(**item.dict())
    db.add(db_object)
    await db.commit()

    return db_object


async def edit_product(
    db: AsyncSession,
    product_id: int,
    item: ProductCreate
) -> Product:
    db_object = (
        await db.execute(
            select(Product)
            .filter(Product.id == product_id)
        )
    ).scalars().first()

    if db_object is not None:
        for var, value in item.dict().items():
            setattr(db_object, var, value) if value is not None else None

        db_object.modified = True
        db.add(db_object)
        await db.commit()

    return db_object


async def delete_product(
    db: AsyncSession,
    product_id: int
) -> None:
    await db.execute(
        delete(Product)
        .filter(Product.id == product_id)
    )
    await db.commit()
