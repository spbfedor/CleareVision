import pytest

from src.service_layer.services import UserProfileService
from tests.unit.service_layer.fakes import FakeUserProfileRepository


@pytest.mark.asyncio(loop_scope="function")
async def test_can_save_profile():
    repo = FakeUserProfileRepository()
    service = UserProfileService(repo)
    await service.save_profile(
        user_id="user_1", font_size=2.0, visual_mode="normal", letter_spacing=0.0
    )

    saved_profile = await repo.get("user_1")
    assert saved_profile is not None
