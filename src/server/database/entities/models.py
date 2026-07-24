from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Song(Base):
    __tablename__ = "songs"

    song_id = Column(String(32), primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    uploader = Column(Text)
    duration = Column(Integer)
    upload_date = Column(String(16))
    description = Column(Text)
    url = Column(Text)
    thumbnail = Column(Text)
    isrc = Column(String(32), nullable=True)
    upc = Column(String(32), nullable=True)
    musicbrainz_recording_id = Column(String(64), nullable=True)
    musicbrainz_release_id = Column(String(64), nullable=True)
    musicbrainz_artist_ids = Column(JSON, nullable=True)
    spotify_id = Column(String(128), nullable=True)
    deezer_id = Column(String(128), nullable=True)
    apple_music_id = Column(String(128), nullable=True)
    youtube_video_id = Column(String(32), nullable=True)
    spotify = Column(Text, nullable=True)
    deezer = Column(Text, nullable=True)
    apple_music = Column(Text, nullable=True)
    youtube = Column(Text, nullable=True)
    musicbrainz = Column(Text, nullable=True)
    lastfm = Column(Text, nullable=True)
    genius = Column(Text, nullable=True)
    copyright = Column(Text, nullable=True)
    phonographic = Column(Text, nullable=True)
    publisher = Column(Text, nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    size_bytes = Column(BigInteger)
    size_mb = Column(Numeric(12, 2), nullable=True)
    downloaded = Column(Boolean, nullable=False, default=False)
    visualizer_data = Column(JSON, nullable=True, default=dict)
    metadata_created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    playlists = relationship("PlaylistSong", back_populates="song")
    ytb_metadata = relationship("YtbMetadata", back_populates="song", uselist=False)


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    stage_name = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=True, unique=True)
    channel_id = Column(String(128), nullable=True, unique=True)
    spotify_id = Column(String(128), nullable=True)
    apple_music_id = Column(String(128), nullable=True)
    soundcloud_id = Column(String(128), nullable=True)
    youtube_url = Column(Text, nullable=True)
    website_url = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    banner_url = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    country_code = Column(String(2), nullable=True)
    genres = Column(JSON, nullable=True)
    followers_count = Column(BigInteger, nullable=True)
    monthly_listeners = Column(BigInteger, nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    albums = relationship("Album", back_populates="artist")
    album_credits = relationship("AlbumArtist", back_populates="artist")


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey("artists.artist_id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True, unique=True)
    album_type = Column(String(32), nullable=True)
    release_date = Column(Date, nullable=True)
    cover_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    track_count = Column(Integer, nullable=True)
    total_duration = Column(Integer, nullable=True)
    total_size_mb = Column(Numeric(12, 2), nullable=True)
    is_explicit = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    artist = relationship("Artist", back_populates="albums")
    credits = relationship("AlbumArtist", back_populates="album")


class AlbumArtist(Base):
    __tablename__ = "album_artists"

    album_id = Column(BigInteger, ForeignKey("albums.album_id", ondelete="CASCADE"), primary_key=True)
    artist_id = Column(BigInteger, ForeignKey("artists.artist_id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(64), primary_key=True)
    credit_order = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    album = relationship("Album", back_populates="credits")
    artist = relationship("Artist", back_populates="album_credits")


class Classification(Base):
    __tablename__ = "classifications"

    classification_id = Column(BigInteger, primary_key=True, autoincrement=True)
    genre = Column(String(128), nullable=True)
    subgenres = Column(JSON, nullable=True)
    moods = Column(JSON, nullable=True)
    language = Column(String(64), nullable=True)
    is_explicit = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )


class YtbMetadata(Base):
    __tablename__ = "ytb_metadata"

    song_id = Column(String(32), ForeignKey("songs.song_id", ondelete="CASCADE"), primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    uploader = Column(Text)
    duration = Column(Integer)
    upload_date = Column(String(16))
    description = Column(Text)
    url = Column(Text)
    thumbnail = Column(Text)
    size_bytes = Column(BigInteger)
    size_mb = Column(Numeric(12, 2), nullable=True)
    metadata_created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    song = relationship("Song", back_populates="ytb_metadata")


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
    song_id = Column(String(32), ForeignKey("songs.song_id", ondelete="CASCADE"), primary_key=True)
    position = Column(Integer, nullable=False)

    playlist = relationship("Playlist", back_populates="songs")
    song = relationship("Song", back_populates="playlists")
