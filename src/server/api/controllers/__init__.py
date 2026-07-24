from .albums import router as albums_router
from .artists import router as artists_router
from .classifications import router as classifications_router
from .playlists import router as playlists_router
from .songs import router as songs_router

__all__ = [
	"songs_router",
	"artists_router",
	"albums_router",
	"classifications_router",
	"playlists_router",
]
