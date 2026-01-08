import pytest_asyncio
from fastapi import Depends
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session, sqla_uow
from app.infrastructure.models.sqla import Base
from app.infrastructure.uow.sqla import SqlAlchemyUnitOfWork
from main import app
from tests.db import AsyncSessionTest, engine


async def override_get_async_session():
    async with AsyncSessionTest() as session:
        yield session


async def override_sqla_uow(
    session=Depends(override_get_async_session),
):
    return SqlAlchemyUnitOfWork(session)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Создание всех таблиц перед запуском тестов"""
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    yield
    print("Dropping database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Database tables dropped")


@pytest_asyncio.fixture(scope="class")
async def db_session():
    """Фикстура сессии с областью видимости класса"""
    async with AsyncSessionTest() as session:
        yield session


@pytest_asyncio.fixture(scope="class")
async def async_client(db_session: AsyncSession):
    """Фикстура клиента с общей сессией для всех тестов класса"""

    async def override_get_async_session():
        yield db_session

    async def override_sqla_uow(
        session: AsyncSession = Depends(override_get_async_session),
    ):
        return SqlAlchemyUnitOfWork(session)

    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[sqla_uow] = override_sqla_uow

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()
