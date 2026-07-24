from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class YtbMetadataBase(BaseModel):
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


class YtbMetadataCreate(YtbMetadataBase):
    pass


class YtbMetadataUpdate(BaseModel):
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


class YtbMetadataRead(YtbMetadataBase):
    song_id: str
    metadata_created_at: Optional[datetime] = None

    class Config:
        orm_mode = True