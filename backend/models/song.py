from sqlalchemy import Column, String, Float, Integer
from backend.db.base import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    title_lower = Column(String, index=True)

    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    loudness = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)

    duration_ms = Column(Integer, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    num_sections = Column(Integer, nullable=True)
    num_segments = Column(Integer, nullable=True)

    rating = Column(Integer, nullable=True)
