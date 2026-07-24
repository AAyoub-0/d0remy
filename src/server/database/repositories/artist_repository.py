from sqlalchemy.orm import Session

from ..entities.models import Artist


def create_artist(session: Session, artist_data: dict) -> Artist:
    artist = Artist(**artist_data)
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


def get_artist(session: Session, artist_id: int) -> Artist | None:
    return session.get(Artist, artist_id)


def list_artists(session: Session, limit: int = 100) -> list[Artist]:
    return session.query(Artist).limit(limit).all()