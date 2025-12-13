from pydantic import BaseModel
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