from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.adapters.orm import Base
from src.adapters.repository import UserProfileRepository
from src.config import settings
from src.entrypoints.schemas import ProfileCreateSchema
from src.service_layer.services import UserProfileService

engine = create_async_engine(
    settings.database_url,
    connect_args={"ssl": "disable"}
)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="ClearVision API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_service():
    async with async_session_maker() as session:
        yield UserProfileService(UserProfileRepository(session))
        await session.commit()


@app.post("/profile/", status_code=status.HTTP_201_CREATED)
async def create_profile(
    data: ProfileCreateSchema,
    service: UserProfileService = Depends(get_service)
):
    await service.save_profile(
        user_id=data.user_id,
        font_size=data.font_size,
        visual_mode=data.visual_mode,
        letter_spacing=data.letter_spacing,
    )
    return {"user_id": data.user_id, "status": "success"}


@app.get("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def get_profile(
    user_id: str,
    service: UserProfileService = Depends(get_service)
):
    profile = await service.repository.get(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return {
        "user_id": profile.user_id,
        "font_size": profile.font_size,
        "visual_mode": profile.visual_mode,
        "letter_spacing": profile.letter_spacing,
    }


app.mount("/static", StaticFiles(directory="src/static"), name="static")
