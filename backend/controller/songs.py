from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_db
from backend.schemas.song import SongView
from backend.services.song_service import SongService

router = APIRouter(prefix='/songs', tags=["songs"])

async def get_service(db: AsyncSession = Depends(get_db)):
    return SongService(db= db)

@router.get('/', response_model= list[SongView])
async def list_songs(skip: int = 0, limit: int = 10, service: SongService = Depends(get_service)):
    songs_list = await service.list_songs(skip= skip, limit= limit)
    return songs_list

@router.get("/search", response_model=SongView)
async def get_song(title: str = Query(..., min_length=1), service: SongService = Depends(get_service)):
    song = await service.get_song_by_title(title)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.post("/{song_id}/rate")
async def rate_song(song_id: int, rating: int = Query(..., ge=1, le=5), service: SongService = Depends(get_service)):
    try:
        updated = await service.rate_song(song_id, rating)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"id": updated.id, "rating": updated.rating}