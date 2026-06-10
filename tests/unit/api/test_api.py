import pytest

from src.domain import UserProfile


@pytest.mark.asyncio(loop_scope="function")
async def test_sending_a_request_to_a_route(client):
    async_client, repo = client

    payload = {"user_id": "user_1", "font_size": 2.0}
    response = await async_client.post("/profile/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "user_1"
    assert data["status"] == "success"


@pytest.mark.asyncio(loop_scope="function")
async def test_can_retrieve_existing_profile(client):
    async_client, repo = client

    existing_profile = UserProfile(
        user_id="user_get_1",
        font_size=2.5,
        visual_mode="monochrome",
        letter_spacing=0.5,
    )
    await repo.add(existing_profile)

    response = await async_client.get("/profile/user_get_1")
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == "user_get_1"
    assert data["font_size"] == 2.5
    assert data["visual_mode"] == "monochrome"
    assert data["letter_spacing"] == 0.5
