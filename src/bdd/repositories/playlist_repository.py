from sqlalchemy.orm import Session

from ..entities.models import Playlist, PlaylistSong


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
