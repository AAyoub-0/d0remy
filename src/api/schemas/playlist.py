from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PlaylistBase(BaseModel):
    title: Optional[str] = None
    uploader: Optional[str] = None
    uploader_id: Optional[str] = None
    webpage_url: Optional[str] = None
    description: Optional[str] = None
    entry_count: Optional[int] = None
    total_size_mb: Optional[float] = None


class PlaylistCreate(PlaylistBase):
    playlist_id: str


class PlaylistUpdate(BaseModel):
    title: Optional[str] = None
    uploader: Optional[str] = None
    uploader_id: Optional[str] = None
    webpage_url: Optional[str] = None
    description: Optional[str] = None
    entry_count: Optional[int] = None
    total_size_mb: Optional[float] = None


class PlaylistRead(PlaylistBase):
    playlist_id: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PlaylistSongCreate(BaseModel):
    video_id: str
    position: int


class PlaylistSongRead(BaseModel):
    playlist_id: str
    video_id: str
    position: int

    class Config:
        orm_mode = True
