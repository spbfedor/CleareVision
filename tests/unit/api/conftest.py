import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.entrypoints.fastapi_app import app, get_service
from src.service_layer.services import UserProfileService
from tests.unit.service_layer.fakes import FakeUserProfileRepository


@pytest_asyncio.fixture(loop_scope="function")
async def client():
    fake_repo = FakeUserProfileRepository()
    fake_service = UserProfileService(fake_repo)

    app.dependency_overrides[get_service] = lambda: fake_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac, fake_repo

    app.dependency_overrides.clear()
