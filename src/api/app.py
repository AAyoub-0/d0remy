from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .controllers.playlists import router as playlists_router
from .controllers.songs import router as songs_router

app = FastAPI(title="YouTube Music Downloader API")
app.include_router(songs_router)
app.include_router(playlists_router)


@app.get("/", include_in_schema=False)
def root_redirect():
	"""Redirect root to the automatic Swagger UI at /docs"""
	return RedirectResponse(url="/docs")
