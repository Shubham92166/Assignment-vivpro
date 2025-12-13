from sqlalchemy import select, update
from models.song import Song

class SongRepository:
    """
    Repository class for performing CRUD operations on Song entities.
    Provides helper methods for listing songs, retrieving by filters,
    and updating attributes.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session.

        Args:
            db: The async SQLAlchemy session to interact with the database.
        """
        self.db = db

    async def list_songs(self, skip: int = 0, limit: int = 10):
        """
        Retrieve a paginated list of songs.

        Args:
            skip (int): Number of records to skip (offset). Default is 0.
            limit (int): Maximum number of records to return. Default is 10.

        Returns:
            list[Song]: List of Song objects.
        """
        query = select(Song).offset(skip).limit(limit)
        response = await self.db.execute(query)
        return response.scalars().all()

    async def get_Song_by_id(self, song_id: int):
        """
        Retrieve a single song by its ID.

        Args:
            song_id (int): Unique ID of the song.

        Returns:
            Song | None: Song object if found, otherwise None.
        """
        query = select(Song).where(Song.id == song_id)
        response = await self.db.execute(query)
        return response.scalars().first()

    async def get_song_by_title(self, song_title: str):
        """
        Retrieve the first song that contains the given title substring.

        Args:
            song_title (str): Case-insensitive substring of the song title.

        Returns:
            Song | None: First matching Song object, or None if no match found.
        """
        query = select(Song).where(Song.title_lower.contains(song_title.lower()))
        response = await self.db.execute(query)
        return response.scalars().first()

    async def update_rating(self, rating: int, song_id: int):
        """
        Update the rating of a song and return the updated record.

        Args:
            rating (int): New rating to assign.
            song_id (int): ID of the song to update.

        Returns:
            Song | None: Updated Song object, or None if not found.
        """
        query = update(Song).where(Song.id == song_id).values(rating=rating)
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_Song_by_id(song_id)
