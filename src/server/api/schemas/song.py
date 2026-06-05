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
    size_bytes: Optional[int] = None
    size_mb: Optional[float] = None
    downloaded: Optional[bool] = False


class SongCreate(SongBase):
    video_id: str


class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    uploader: Optional[str] = None
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    size_bytes: Optional[int] = None
    size_mb: Optional[float] = None
    downloaded: Optional[bool] = None


class SongRead(SongBase):
    video_id: str
    metadata_created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
