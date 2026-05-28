from sqlalchemy import Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class UserProfileOrm(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(String, primary_key=True)
    font_size: Mapped[float] = mapped_column(Float)
    visual_mode: Mapped[str] = mapped_column(String)
    letter_spacing: Mapped[float] = mapped_column(Float)
