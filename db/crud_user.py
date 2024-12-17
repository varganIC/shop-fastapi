from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.users import User
from schemas.auth import UserCreate


async def get_user(db: AsyncSession, username: str):
    query = (
        await db.execute(
            select(User)
            .filter(User.username == username)
        )
    ).scalars().first()

    return query


async def create_user(db: AsyncSession, item: UserCreate):
    db_object = User(**item.dict())
    db.add(db_object)
    await db.commit()

    return db_object
