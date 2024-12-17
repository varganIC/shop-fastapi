from sqlalchemy import (
    and_,
    delete,
    func
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.bucket import Bucket
from db.models.products import Product
from schemas.bucket import BucketAdd, BucketCreate


async def bucket_add(
    db: AsyncSession,
    item: BucketAdd,
    user_id: int
) -> Bucket:
    db_object = (
        await db.execute(
            select(Bucket)
            .filter(
                and_(
                    Bucket.user_id == user_id,
                    Bucket.product_id == item.product_id
                )
            )
        )
    ).scalars().first()

    if db_object is not None:
        db_object.quantity += 1
        db_object.modified = True
        db.add(db_object)
        await db.commit()

        return db_object

    db_object = Bucket(**item.dict(), user_id=user_id)
    db.add(db_object)
    await db.commit()

    return db_object


async def bucket_edit(
    db: AsyncSession,
    item: BucketCreate,
    user_id: int
) -> Bucket:
    db_object = (
        await db.execute(
            select(Bucket)
            .filter(
                and_(
                    Bucket.user_id == user_id,
                    Bucket.product_id == item.product_id
                )
            )
        )
    ).scalars().first()

    if db_object is not None:
        db_object.quantity = item.quantity

        db_object.modified = True
        db.add(db_object)
        await db.commit()

    return db_object


async def bucket_delete(
    db: AsyncSession,
    product_id: int,
    user_id: int
) -> None:
    await db.execute(
        delete(Bucket)
        .filter(
            and_(
                Bucket.user_id == user_id,
                Bucket.product_id == product_id
            )
        )
    )
    await db.commit()


async def bucket_clear_all(
    db: AsyncSession,
    user_id: int
) -> None:
    await db.execute(
        delete(Bucket)
        .filter(
            Bucket.user_id == user_id
        )
    )
    await db.commit()


async def get_amount_cost_bucket(
    db: AsyncSession,
    user_id: int
):
    query = (
        await db.execute(
            select(
                func.sum(Bucket.quantity).label("count"),
                func.sum(Product.price * Bucket.quantity).label("amount_cost")
            )
            .join(
                Bucket,
                Product.id == Bucket.product_id
            )
            .filter(
                Bucket.user_id == user_id
            )
        )
    ).all()

    return query
