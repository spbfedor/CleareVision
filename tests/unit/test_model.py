import pytest
from src.domain import UserProfile


def test_settings_creations_with_valid_data():
    profile = UserProfile(
        user_id="id_1",
        font_size=2.0,
        visual_mode="normal",
        letter_spacing=1.0
    )
    assert profile.user_id == "id_1"
    assert profile.font_size == 2.0
    assert profile.visual_mode == "normal"
    assert profile.letter_spacing == 1.0


def test_default_values():
    with pytest.raises(TypeError):
        UserProfile(user_id="id_1")
