from pydantic import BaseModel


class ProfileCreateSchema(BaseModel):
    user_id: str
    font_size: float = 1.0
    visual_mode: str = "normal"
    letter_spacing: float = 0.0
