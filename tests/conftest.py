from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport



import pytest


from app.main import app
from app.database.models import TaskTable, UserTable
from app.database.models.base import Base
from app.database.depends import get_db
from app.security.login import get_current_user_by_id


TEST_BASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/todo_test"
engine = create_async_engine(TEST_BASE_URL)

TestSession = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
async def create_delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def get_sess():
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            async with TestSession(bind=connection, expire_on_commit=False) as session:
                await session.begin_nested()

                yield session

                await transaction.rollback()


@pytest.fixture
async def test_client(get_sess):
    app.dependency_overrides[get_db] = lambda: get_sess
    app.dependency_overrides[get_current_user_by_id] = lambda: 67

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
