from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm import UserProfileOrm
from src.domain import UserProfile


class UserProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, profile):
        orm_profile = UserProfileOrm(
            user_id=profile.user_id,
            font_size=profile.font_size,
            visual_mode=profile.visual_mode,
            letter_spacing=profile.letter_spacing,
        )
        self.session.add(orm_profile)

    async def get(self, user_id):
        query = select(UserProfileOrm).where(UserProfileOrm.user_id == user_id)
        result = await self.session.execute(query)
        orm_profile = result.scalar_one_or_none()
        if orm_profile is not None:
            return UserProfile(
                user_id=orm_profile.user_id,
                font_size=orm_profile.font_size,
                visual_mode=orm_profile.visual_mode,
                letter_spacing=orm_profile.letter_spacing,
            )
        else:
            return None
