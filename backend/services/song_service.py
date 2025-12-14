from backend.repositories.song_repository import SongRepository

class SongService:
    """
    Service layer for handling business logic related to songs.
    Communicates with SongRepository for database operations.
    """

    def __init__(self, db):
        """
        Initialize the song service with a database session.

        Args:
            db: Async SQLAlchemy session object.
        """
        self.song_repository = SongRepository(db= db)
    
    async def list_songs(self, skip: int = 0, limit: int = 10):
        """
        Retrieve a paginated list of songs.

        Args:
            skip (int): Number of records to skip. Default is 0.
            limit (int): Number of records to return. Default is 10.

        Returns:
            list[Song]: A list of Song objects.
        """
        return await self.song_repository.list_songs(skip=skip, limit=limit)
    
    async def get_song_by_title(self, song_title: str):
        """
        Retrieve the first song whose title contains the given text.

        Args:
            song_title (str): Partial or complete song title (case-insensitive).

        Returns:
            Song | None: First matching Song object, else None.
        """
        return await self.song_repository.get_song_by_title(song_title=song_title)
    
    async def rate_song(self, song_id: int, rating: int):
        """
        Update the rating of a song.

        Args:
            rating (int): Rating value (must be between 1 and 5).
            song_id (int): ID of the song to update.

        Raises:
            ValueError: If rating is not between 1 and 5.

        Returns:
            Song | None: The updated Song object, or None if song not found.
        """
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 to 5!")

        return await self.song_repository.update_rating(song_id=song_id, rating=rating)