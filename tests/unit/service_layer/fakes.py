from src.domain import UserProfile

class FakeUserProfileRepository:
    def __init__(self):
        self._profiles = []

    async def add(self, profile: UserProfile) -> None:
        self._profiles.append(profile)

    async def get(self, user_id: str) -> UserProfile | None:
        for p in self._profiles:
            if p.user_id == user_id:
                return p
        return None
