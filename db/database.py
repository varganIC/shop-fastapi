from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings.settings_loader import db_settings

SQLALCHEMY_DATABASE_URL_ASYNC = (
    db_settings.sql_alchemy_conn_string_async()
)

engine_async = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC,
    echo=False,
    future=True
)

SessionLocalAsync = sessionmaker(
    engine_async, class_=AsyncSession, expire_on_commit=False,
)


async def get_db_async() -> AsyncSession:
    async with SessionLocalAsync() as session:
        yield session
