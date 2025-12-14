import pytest
from backend.services.song_service import SongService
from backend.models.song import Song


@pytest.mark.asyncio
async def test_rate_song_success(db_session):
    song = Song(title="Test Song", rating=3)
    db_session.add(song)
    await db_session.commit()
    await db_session.refresh(song)

    service = SongService(db=db_session)
    updated = await service.rate_song(song.id, 5)

    assert updated.rating == 5


@pytest.mark.asyncio
async def test_rate_song_not_found(db_session):
    service = SongService(db=db_session)
    result = await service.rate_song(999, 4)

    assert result is None


@pytest.mark.asyncio
async def test_rate_song_invalid_rating(db_session):
    song = Song(title="Bad Song", rating=3)
    db_session.add(song)
    await db_session.commit()
    await db_session.refresh(song)

    service = SongService(db=db_session)

    with pytest.raises(ValueError):
        await service.rate_song(song.id, 10)


@pytest.mark.asyncio
async def test_list_songs(db_session):
    db_session.add_all([
        Song(title="A"),
        Song(title="B"),
        Song(title="C"),
    ])
    await db_session.commit()

    service = SongService(db=db_session)
    songs = await service.list_songs(skip=0, limit=10)

    assert len(songs) >= 3


@pytest.mark.asyncio
async def test_list_songs_large_skip(db_session):
    service = SongService(db=db_session)
    songs = await service.list_songs(skip=1000, limit=10)

    assert songs == []
