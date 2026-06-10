from dataclasses import dataclass, field


@dataclass
class UserProfile:
    user_id: str
    font_size: float = field(default=1.0)
    visual_mode: str = field(default="normal")
    letter_spacing: float = field(default=0.0)

    def __post_init__(self):
        if self.font_size > 3.0:
            raise ValueError("Error: field value cannot be greater than '3'")

        valid_modes = ["normal", "monochrome", "inverted"]

        if self.visual_mode not in valid_modes:
            raise ValueError("Error: invalid visual mode")
