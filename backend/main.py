from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.controller.songs import router as songs_router
from backend.db.base import Base
from backend.db.session import engine
from backend.middlewares.request_id import request_id_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Backend Service - Songs",
    lifespan=lifespan
)

app.middleware("http")(request_id_middleware)

app.include_router(songs_router, prefix="/api/v1")