import pytest

from src.adapters import UserProfileRepository
from src.domain import UserProfile


@pytest.mark.asyncio(loop_scope="function")
async def test_repository_contract(session):
    profile = UserProfile(
        user_id="user1",
        font_size=2.0,
        visual_mode="normal",
        letter_spacing=0.0
    )
    repository = UserProfileRepository(session)
    await repository.add(profile)
    await session.flush()
    prodile_from_db = await repository.get("user1")
    assert profile == prodile_from_db
