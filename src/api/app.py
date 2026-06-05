from fastapi import FastAPI

from .controllers.playlists import router as playlists_router
from .controllers.songs import router as songs_router

app = FastAPI(title="YouTube Music Downloader API")
app.include_router(songs_router)
app.include_router(playlists_router)
