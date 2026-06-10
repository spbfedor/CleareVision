import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.adapters.orm import Base
from src.config import settings


@pytest_asyncio.fixture(loop_scope="function")
async def fixt_engine():
    engine = create_async_engine(settings.database_url, connect_args={"ssl": "disable"})

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(loop_scope="function")
async def session(fixt_engine):
    async_session = async_sessionmaker(bind=fixt_engine, expire_on_commit=False)
    async with async_session() as session_obj:
        yield session_obj
