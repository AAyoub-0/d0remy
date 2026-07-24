from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class AlbumBase(BaseModel):
    artist_id: Optional[int] = None
    title: str
    slug: Optional[str] = None
    album_type: Optional[str] = None
    release_date: Optional[date] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    track_count: Optional[int] = None
    total_duration: Optional[int] = None
    total_size_mb: Optional[float] = None
    is_explicit: Optional[bool] = False


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    artist_id: Optional[int] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    album_type: Optional[str] = None
    release_date: Optional[date] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    track_count: Optional[int] = None
    total_duration: Optional[int] = None
    total_size_mb: Optional[float] = None
    is_explicit: Optional[bool] = None


class AlbumRead(AlbumBase):
    album_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AlbumArtistCreate(BaseModel):
    artist_id: int
    role: str
    credit_order: int = 1


class AlbumArtistRead(BaseModel):
    album_id: int
    artist_id: int
    role: str
    credit_order: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True