from .album import AlbumArtistCreate, AlbumArtistRead, AlbumCreate, AlbumRead, AlbumUpdate
from .artist import ArtistBase, ArtistCreate, ArtistRead, ArtistUpdate
from .classification import ClassificationBase, ClassificationCreate, ClassificationRead, ClassificationUpdate
from .playlist import (
    PlaylistBase,
    PlaylistCreate,
    PlaylistRead,
    PlaylistSongCreate,
    PlaylistSongRead,
    PlaylistUpdate,
)
from .song import SongBase, SongCreate, SongRead, SongUpdate
from .ytb_metadata import YtbMetadataBase, YtbMetadataCreate, YtbMetadataRead, YtbMetadataUpdate

__all__ = [
    "SongBase",
    "SongCreate",
    "SongRead",
    "SongUpdate",
    "YtbMetadataBase",
    "YtbMetadataCreate",
    "YtbMetadataRead",
    "YtbMetadataUpdate",
    "ArtistBase",
    "ArtistCreate",
    "ArtistRead",
    "ArtistUpdate",
    "AlbumCreate",
    "AlbumRead",
    "AlbumUpdate",
    "AlbumArtistCreate",
    "AlbumArtistRead",
    "ClassificationBase",
    "ClassificationCreate",
    "ClassificationRead",
    "ClassificationUpdate",
    "PlaylistBase",
    "PlaylistCreate",
    "PlaylistRead",
    "PlaylistSongCreate",
    "PlaylistSongRead",
    "PlaylistUpdate",
]
