from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import SongCreate, SongRead, SongUpdate
from ...database.repositories.song_repository import (
    create_or_update_song,
    get_song,
    list_songs,
)

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("", response_model=List[SongRead])
def read_songs(db: Session = Depends(get_db)):
    return list_songs(db)


@router.post("", response_model=SongRead, status_code=201)
def create_song_endpoint(song: SongCreate, db: Session = Depends(get_db)):
    existing = get_song(db, song.video_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="La chanson existe déjà")
    return create_or_update_song(db, song.dict())


@router.get("/{video_id}", response_model=SongRead)
def read_song(video_id: str, db: Session = Depends(get_db)):
    song = get_song(db, video_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    return song


@router.put("/{video_id}", response_model=SongRead)
def update_song(video_id: str, song_update: SongUpdate, db: Session = Depends(get_db)):
    song = get_song(db, video_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    update_data = song_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(song, key, value)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


@router.delete("/{video_id}", status_code=204)
def delete_song(video_id: str, db: Session = Depends(get_db)):
    song = get_song(db, video_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    db.delete(song)
    db.commit()
