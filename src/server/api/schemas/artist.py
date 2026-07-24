from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArtistBase(BaseModel):
    name: str
    stage_name: Optional[str] = None
    slug: Optional[str] = None
    channel_id: Optional[str] = None
    spotify_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    soundcloud_id: Optional[str] = None
    youtube_url: Optional[str] = None
    website_url: Optional[str] = None
    avatar_url: Optional[str] = None
    banner_url: Optional[str] = None
    bio: Optional[str] = None
    country_code: Optional[str] = None
    genres: Optional[list[str]] = None
    followers_count: Optional[int] = None
    monthly_listeners: Optional[int] = None
    is_verified: Optional[bool] = False


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    stage_name: Optional[str] = None
    slug: Optional[str] = None
    channel_id: Optional[str] = None
    spotify_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    soundcloud_id: Optional[str] = None
    youtube_url: Optional[str] = None
    website_url: Optional[str] = None
    avatar_url: Optional[str] = None
    banner_url: Optional[str] = None
    bio: Optional[str] = None
    country_code: Optional[str] = None
    genres: Optional[list[str]] = None
    followers_count: Optional[int] = None
    monthly_listeners: Optional[int] = None
    is_verified: Optional[bool] = None


class ArtistRead(ArtistBase):
    artist_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True