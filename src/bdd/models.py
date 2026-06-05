from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Song(Base):
    __tablename__ = "songs"

    video_id = Column(String(32), primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    uploader = Column(Text)
    duration = Column(Integer)
    upload_date = Column(String(16))
    description = Column(Text)
    url = Column(Text)
    thumbnail = Column(Text)
    size_bytes = Column(BigInteger)
    size_mb = Column(String(64))
    downloaded = Column(Boolean, nullable=False, default=False)
    metadata_created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    playlists = relationship("PlaylistSong", back_populates="song")


class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column(String(64), primary_key=True)
    title = Column(Text)
    uploader = Column(Text)
    uploader_id = Column(Text)
    webpage_url = Column(Text)
    description = Column(Text)
    entry_count = Column(Integer)
    total_size_mb = Column(String(64))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    songs = relationship("PlaylistSong", back_populates="playlist")


class PlaylistSong(Base):
    __tablename__ = "playlist_songs"

    playlist_id = Column(String(64), ForeignKey("playlists.playlist_id", ondelete="CASCADE"), primary_key=True)
    video_id = Column(String(32), ForeignKey("songs.video_id", ondelete="CASCADE"), primary_key=True)
    position = Column(Integer, nullable=False)

    playlist = relationship("Playlist", back_populates="songs")
    song = relationship("Song", back_populates="playlists")
