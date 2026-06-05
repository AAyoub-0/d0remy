from sqlalchemy.orm import Session

from ..entities.models import Song


def get_song(session: Session, video_id: str) -> Song | None:
    return session.get(Song, video_id)


def is_song_downloaded(session: Session, video_id: str) -> bool:
    song = get_song(session, video_id)
    return bool(song and song.downloaded)


def create_or_update_song(session: Session, song_data: dict) -> Song:
    video_id = song_data["video_id"]
    song = get_song(session, video_id)
    if song is None:
        song = Song(**song_data)
        session.add(song)
    else:
        for key, value in song_data.items():
            if key == "downloaded":
                if value:
                    song.downloaded = True
                continue
            setattr(song, key, value)
        session.add(song)
    session.commit()
    session.refresh(song)
    return song


def create_song(session: Session, song_data: dict) -> Song:
    song = Song(**song_data)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song


def list_songs(session: Session, limit: int = 100) -> list[Song]:
    return session.query(Song).limit(limit).all()


def mark_song_downloaded(session: Session, video_id: str, downloaded: bool = True) -> Song | None:
    song = get_song(session, video_id)
    if song is None:
        return None
    song.downloaded = downloaded
    session.add(song)
    session.commit()
    session.refresh(song)
    return song
