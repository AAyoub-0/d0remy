from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import AlbumArtistCreate, AlbumArtistRead, AlbumCreate, AlbumRead, AlbumUpdate
from ...database.entities.models import AlbumArtist
from ...database.repositories.album_repository import add_artist_to_album, create_album, get_album, list_album_artists, list_albums
from ...database.repositories.artist_repository import get_artist

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("", response_model=List[AlbumRead])
def read_albums(db: Session = Depends(get_db)):
    return list_albums(db)


@router.post("", response_model=AlbumRead, status_code=201)
def create_album_endpoint(album: AlbumCreate, db: Session = Depends(get_db)):
    if album.artist_id is not None and get_artist(db, album.artist_id) is None:
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    return create_album(db, album.dict())


@router.get("/{album_id}", response_model=AlbumRead)
def read_album(album_id: int, db: Session = Depends(get_db)):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="Album introuvable")
    return album


@router.put("/{album_id}", response_model=AlbumRead)
def update_album(album_id: int, album_update: AlbumUpdate, db: Session = Depends(get_db)):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="Album introuvable")
    update_data = album_update.dict(exclude_unset=True)
    artist_id = update_data.get("artist_id")
    if artist_id is not None and get_artist(db, artist_id) is None:
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    for key, value in update_data.items():
        setattr(album, key, value)
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}", status_code=204)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="Album introuvable")
    db.delete(album)
    db.commit()


@router.get("/{album_id}/artists", response_model=List[AlbumArtistRead])
def read_album_artists(album_id: int, db: Session = Depends(get_db)):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="Album introuvable")
    return list_album_artists(db, album_id)


@router.post("/{album_id}/artists", response_model=AlbumArtistRead, status_code=201)
def add_album_artist_endpoint(album_id: int, payload: AlbumArtistCreate, db: Session = Depends(get_db)):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="Album introuvable")
    artist = get_artist(db, payload.artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    existing = db.query(AlbumArtist).filter_by(album_id=album_id, artist_id=payload.artist_id, role=payload.role).one_or_none()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Crédit album déjà existant")
    return add_artist_to_album(db, album_id, payload.artist_id, payload.role, payload.credit_order)