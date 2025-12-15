from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_db
from backend.services.song_service import SongService
from backend.schemas.pagination import PaginationParams
from backend.schemas.song import (
    SongView,
    SongSearchParams,
    SongRateRequest
)

router = APIRouter(prefix='/songs', tags=["songs"])

async def get_service(db: AsyncSession = Depends(get_db)):
    return SongService(db= db)

@router.get('/', response_model= list[SongView])
async def list_songs(
    payload: PaginationParams = Depends(),
    service: SongService = Depends(get_service)):
    """
    List songs with pagination support.

    Args:
        payload (PaginationParams): Pagination parameters containing
            skip and limit values.
        service (SongService): Song service dependency.

    Returns:
        list[SongView]: A list of songs based on pagination.
    """

    songs_list = await service.list_songs(skip= payload.skip, limit= payload.limit)
    return songs_list

@router.get("/search", response_model=SongView)
async def get_song(
    payload: SongSearchParams = Depends(),
    service: SongService = Depends(get_service)):

    """
    Rate an existing song.

    Args:
        song_id (int): Unique ID of the song to be rated.
        payload (SongRateRequest): Rating payload containing value between 1 and 5.
        service (SongService): Song service dependency.

    Returns:
        dict: Updated song ID and rating.

    Raises:
        HTTPException:
            - 400 if rating is invalid.
            - 404 if song does not exist.
    """
    
    song = await service.get_song_by_title(payload.title)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song

@router.post("/{song_id}/rate")
async def rate_song(
    song_id: int, payload: SongRateRequest,
    service: SongService = Depends(get_service)):

    """
    Rate an existing song.

    Args:
        song_id (int): Unique ID of the song to be rated.
        payload (SongRateRequest): Rating payload containing value between 1 and 5.
        service (SongService): Song service dependency.

    Returns:
        dict: Updated song ID and rating.

    Raises:
        HTTPException:
            - 400 if rating is invalid.
            - 404 if song does not exist.
    """

    try:
        updated = await service.rate_song(song_id, payload.rating)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Song not found")
    return {"id": updated.id, "rating": updated.rating}