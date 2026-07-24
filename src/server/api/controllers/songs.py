from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import SongCreate, SongRead, SongUpdate, YtbMetadataCreate, YtbMetadataRead, YtbMetadataUpdate
from ...database.repositories.song_repository import (
    create_or_update_song,
    get_song,
    list_songs,
)
from ...database.repositories.ytb_metadata_repository import (
    create_or_update_ytb_metadata,
    delete_ytb_metadata,
    get_ytb_metadata,
)

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("", response_model=List[SongRead])
def read_songs(db: Session = Depends(get_db)):
    return list_songs(db)


@router.post("", response_model=SongRead, status_code=201)
def create_song_endpoint(song: SongCreate, db: Session = Depends(get_db)):
    existing = get_song(db, song.song_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="La chanson existe déjà")
    return create_or_update_song(db, song.dict())


@router.get("/{song_id}", response_model=SongRead)
def read_song(song_id: str, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    return song


@router.put("/{song_id}", response_model=SongRead)
def update_song(song_id: str, song_update: SongUpdate, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    update_data = song_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(song, key, value)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


@router.delete("/{song_id}", status_code=204)
def delete_song(song_id: str, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    db.delete(song)
    db.commit()


@router.get("/{song_id}/ytb-metadata", response_model=YtbMetadataRead)
def read_song_ytb_metadata(song_id: str, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    metadata = get_ytb_metadata(db, song_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Métadonnées YTB introuvables")
    return metadata


@router.put("/{song_id}/ytb-metadata", response_model=YtbMetadataRead)
def upsert_song_ytb_metadata(song_id: str, payload: YtbMetadataCreate, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    return create_or_update_ytb_metadata(db, song_id, payload.dict())


@router.patch("/{song_id}/ytb-metadata", response_model=YtbMetadataRead)
def patch_song_ytb_metadata(song_id: str, payload: YtbMetadataUpdate, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    metadata = get_ytb_metadata(db, song_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Métadonnées YTB introuvables")
    return create_or_update_ytb_metadata(db, song_id, payload.dict(exclude_unset=True))


@router.delete("/{song_id}/ytb-metadata", status_code=204)
def remove_song_ytb_metadata(song_id: str, db: Session = Depends(get_db)):
    song = get_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chanson introuvable")
    deleted = delete_ytb_metadata(db, song_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Métadonnées YTB introuvables")
