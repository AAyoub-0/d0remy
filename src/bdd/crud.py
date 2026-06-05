from sqlalchemy.orm import Session

from .models import Playlist, PlaylistSong, Song


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


def get_song(session: Session, video_id: str) -> Song | None:
    return session.get(Song, video_id)


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


def create_playlist(session: Session, playlist_data: dict) -> Playlist:
    playlist = Playlist(**playlist_data)
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist


def get_playlist(session: Session, playlist_id: str) -> Playlist | None:
    return session.get(Playlist, playlist_id)


def list_playlists(session: Session, limit: int = 100) -> list[Playlist]:
    return session.query(Playlist).limit(limit).all()


def add_song_to_playlist(session: Session, playlist_id: str, video_id: str, position: int) -> PlaylistSong:
    playlist_song = PlaylistSong(playlist_id=playlist_id, video_id=video_id, position=position)
    session.add(playlist_song)
    session.commit()
    session.refresh(playlist_song)
    return playlist_song


def get_playlist_songs(session: Session, playlist_id: str) -> list[PlaylistSong]:
    playlist = get_playlist(session, playlist_id)
    if playlist is None:
        return []
    return playlist.songs
