from src.domain import UserProfile
from src.adapters.orm import UserProfileOrm 

class UserProfileService:
    def __init__(self, repository):
        self.repository = repository

    async def save_profile(
        self, 
        user_id: str, 
        font_size: float, 
        visual_mode: str, 
        letter_spacing: float
    ) -> None:
        existing_profile = await self.repository.get(user_id)
        
        if existing_profile is not None:
            await self.repository.session.merge(
                UserProfileOrm(
                    user_id=user_id,
                    font_size=font_size,
                    visual_mode=visual_mode,
                    letter_spacing=letter_spacing
                )
            )
        else:
            profile = UserProfile(
                user_id=user_id,
                font_size=font_size,
                visual_mode=visual_mode,
                letter_spacing=letter_spacing
            )
            await self.repository.add(profile)
