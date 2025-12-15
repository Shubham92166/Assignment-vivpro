from pydantic import BaseModel, Field
from typing import Optional

class SongView(BaseModel):
    id: int
    title: Optional[str]
    danceability: Optional[float]
    energy: Optional[float]
    tempo: Optional[float]
    duration_ms: Optional[int]
    duration_seconds: Optional[float]
    num_sections: Optional[int]
    num_segments: Optional[int]
    rating: Optional[int]

    class Config:
        orm_mode = True

class SongSearchParams(BaseModel):
    title: str = Field(..., min_length=1)

class SongRateRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)