from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

from .controllers.playlists import router as playlists_router
from .controllers.songs import router as songs_router

app = FastAPI(title="YouTube Music Downloader API")
app.include_router(songs_router)
app.include_router(playlists_router)

DOWNLOADS_DIR = Path(__file__).resolve().parents[3] / "downloads"

@app.get("/media/{video_id}", include_in_schema=False)
def media(video_id: str):
    video_folder = DOWNLOADS_DIR / video_id
    if not video_folder.exists() or not video_folder.is_dir():
        raise HTTPException(status_code=404, detail="Audio introuvable")

    mp3_files = list(video_folder.glob("*.mp3"))
    if not mp3_files:
        raise HTTPException(status_code=404, detail="Audio introuvable")

    return FileResponse(mp3_files[0], media_type="audio/mpeg", filename=mp3_files[0].name)


@app.get("/", include_in_schema=False)
def root_redirect():
	"""Redirect root to the automatic Swagger UI at /docs"""
	return RedirectResponse(url="/docs")
