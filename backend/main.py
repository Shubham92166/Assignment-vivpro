from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.controller.songs import router as songs_router
from backend.db.base import Base
from backend.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown (optional)
    await engine.dispose()

app = FastAPI(
    title="Song Service - MVC + Prod features",
    lifespan=lifespan
)

app.include_router(songs_router, prefix="/api/v1")