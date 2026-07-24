from sqlalchemy.orm import Session

from ..entities.models import Album, AlbumArtist


def create_album(session: Session, album_data: dict) -> Album:
    album = Album(**album_data)
    session.add(album)
    session.commit()
    session.refresh(album)
    return album


def get_album(session: Session, album_id: int) -> Album | None:
    return session.get(Album, album_id)


def list_albums(session: Session, limit: int = 100) -> list[Album]:
    return session.query(Album).limit(limit).all()


def add_artist_to_album(session: Session, album_id: int, artist_id: int, role: str, credit_order: int = 1) -> AlbumArtist:
    credit = AlbumArtist(album_id=album_id, artist_id=artist_id, role=role, credit_order=credit_order)
    session.add(credit)
    session.commit()
    session.refresh(credit)
    return credit


def list_album_artists(session: Session, album_id: int) -> list[AlbumArtist]:
    return session.query(AlbumArtist).filter_by(album_id=album_id).order_by(AlbumArtist.credit_order.asc()).all()