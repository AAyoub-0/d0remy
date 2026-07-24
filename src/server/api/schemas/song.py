from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SongBase(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    uploader: Optional[str] = None
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    isrc: Optional[str] = None
    upc: Optional[str] = None
    musicbrainz_recording_id: Optional[str] = None
    musicbrainz_release_id: Optional[str] = None
    musicbrainz_artist_ids: Optional[list[str]] = None
    spotify_id: Optional[str] = None
    deezer_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    youtube_video_id: Optional[str] = None
    spotify: Optional[str] = None
    deezer: Optional[str] = None
    apple_music: Optional[str] = None
    youtube: Optional[str] = None
    musicbrainz: Optional[str] = None
    lastfm: Optional[str] = None
    genius: Optional[str] = None
    copyright: Optional[str] = None
    phonographic: Optional[str] = None
    publisher: Optional[str] = None
    rating: Optional[float] = None
    size_bytes: Optional[int] = None
    size_mb: Optional[float] = None
    downloaded: Optional[bool] = False
    visualizer_data: Optional[dict] = None


class SongCreate(SongBase):
    song_id: str


class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    uploader: Optional[str] = None
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    isrc: Optional[str] = None
    upc: Optional[str] = None
    musicbrainz_recording_id: Optional[str] = None
    musicbrainz_release_id: Optional[str] = None
    musicbrainz_artist_ids: Optional[list[str]] = None
    spotify_id: Optional[str] = None
    deezer_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    youtube_video_id: Optional[str] = None
    spotify: Optional[str] = None
    deezer: Optional[str] = None
    apple_music: Optional[str] = None
    youtube: Optional[str] = None
    musicbrainz: Optional[str] = None
    lastfm: Optional[str] = None
    genius: Optional[str] = None
    copyright: Optional[str] = None
    phonographic: Optional[str] = None
    publisher: Optional[str] = None
    rating: Optional[float] = None
    size_bytes: Optional[int] = None
    size_mb: Optional[float] = None
    downloaded: Optional[bool] = None
    visualizer_data: Optional[dict] = None


class SongRead(SongBase):
    song_id: str
    metadata_created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
