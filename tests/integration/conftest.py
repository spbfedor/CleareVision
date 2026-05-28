import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.adapters.orm import Base


@pytest_asyncio.fixture
async def fixt_engine():
    # Отключаем SSL строкой, как требует asyncpg для докера
    engine = create_async_engine(settings.database_url, connect_args={"ssl": "disable"})
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(fixt_engine):
    async_session = async_sessionmaker(
        bind=fixt_engine,
        expire_on_commit=False
    )
    async with async_session() as session_obj:
        yield session_obj
