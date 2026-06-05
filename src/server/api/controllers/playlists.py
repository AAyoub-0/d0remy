from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import (
    PlaylistCreate,
    PlaylistRead,
    PlaylistSongCreate,
    PlaylistSongRead,
    PlaylistUpdate,
)
from ...database.repositories.playlist_repository import (
    add_song_to_playlist,
    create_playlist,
    get_playlist,
    get_playlist_songs,
    list_playlists,
)
from ...database.repositories.song_repository import get_song
from ...database.entities.models import PlaylistSong

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("", response_model=List[PlaylistRead])
def read_playlists(db: Session = Depends(get_db)):
    return list_playlists(db)


@router.post("", response_model=PlaylistRead, status_code=201)
def create_playlist_endpoint(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    existing = get_playlist(db, playlist.playlist_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Playlist existe déjà")
    return create_playlist(db, playlist.dict())


@router.get("/{playlist_id}", response_model=PlaylistRead)
def read_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist introuvable")
    return playlist


@router.put("/{playlist_id}", response_model=PlaylistRead)
def update_playlist(playlist_id: str, playlist_update: PlaylistUpdate, db: Session = Depends(get_db)):
    playlist = get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist introuvable")
    update_data = playlist_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(playlist, key, value)
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


@router.delete("/{playlist_id}", status_code=204)
def delete_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist introuvable")
    db.delete(playlist)
    db.commit()


@router.get("/{playlist_id}/songs", response_model=List[PlaylistSongRead])
def read_playlist_songs(playlist_id: str, db: Session = Depends(get_db)):
    playlist = get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist introuvable")
    return get_playlist_songs(db, playlist_id)


@router.post("/{playlist_id}/songs", response_model=PlaylistSongRead, status_code=201)
def add_song_to_playlist_endpoint(playlist_id: str, playlist_song: PlaylistSongCreate, db: Session = Depends(get_db)):
    playlist = get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist introuvable")
    song = get_song(db, playlist_song.video_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    return add_song_to_playlist(db, playlist_id, playlist_song.video_id, playlist_song.position)


@router.delete("/{playlist_id}/songs/{video_id}", status_code=204)
def delete_song_from_playlist(playlist_id: str, video_id: str, db: Session = Depends(get_db)):
    playlist = get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist introuvable")
    playlist_song = db.query(PlaylistSong).filter_by(playlist_id=playlist_id, video_id=video_id).one_or_none()
    if playlist_song is None:
        raise HTTPException(status_code=404, detail="Chanson de playlist introuvable")
    db.delete(playlist_song)
    db.commit()
