from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import ArtistCreate, ArtistRead, ArtistUpdate
from ...database.repositories.artist_repository import create_artist, get_artist, list_artists

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("", response_model=List[ArtistRead])
def read_artists(db: Session = Depends(get_db)):
    return list_artists(db)


@router.post("", response_model=ArtistRead, status_code=201)
def create_artist_endpoint(artist: ArtistCreate, db: Session = Depends(get_db)):
    return create_artist(db, artist.dict())


@router.get("/{artist_id}", response_model=ArtistRead)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = get_artist(db, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    return artist


@router.put("/{artist_id}", response_model=ArtistRead)
def update_artist(artist_id: int, artist_update: ArtistUpdate, db: Session = Depends(get_db)):
    artist = get_artist(db, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    for key, value in artist_update.dict(exclude_unset=True).items():
        setattr(artist, key, value)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@router.delete("/{artist_id}", status_code=204)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = get_artist(db, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    db.delete(artist)
    db.commit()