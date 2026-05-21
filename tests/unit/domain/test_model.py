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
    profile = UserProfile(user_id="id_1")
    assert profile.user_id == "id_1"
    assert profile.font_size == 1.0
    assert profile.visual_mode == "normal"
    assert profile.letter_spacing == 0.0


def test_font_size_cannot_exceed_gost_limit():
    with pytest.raises(ValueError) as ex:
        UserProfile(user_id="id_1", font_size=3.1)
    assert str(ex.value) == "Error: field value cannot be greater than '3'"


def test_invalid_visual_mode_raises_error():
    with pytest.raises(ValueError) as ex:
        UserProfile(user_id="id_1", visual_mode="broken_mode")
    assert str(ex.value) == "Error: invalid visual mode"
