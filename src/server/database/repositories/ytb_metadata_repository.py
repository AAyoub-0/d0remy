from sqlalchemy.orm import Session

from ..entities.models import YtbMetadata


YTB_METADATA_FIELDS = {
    "title",
    "artist",
    "uploader",
    "duration",
    "upload_date",
    "description",
    "url",
    "thumbnail",
    "size_bytes",
    "size_mb",
}


def get_ytb_metadata(session: Session, song_id: str) -> YtbMetadata | None:
    return session.get(YtbMetadata, song_id)


def create_or_update_ytb_metadata(session: Session, song_id: str, metadata_data: dict) -> YtbMetadata:
    metadata = get_ytb_metadata(session, song_id)
    payload = {key: value for key, value in metadata_data.items() if key in YTB_METADATA_FIELDS}
    payload["song_id"] = song_id
    if metadata is None:
        metadata = YtbMetadata(**payload)
        session.add(metadata)
    else:
        for key, value in payload.items():
            setattr(metadata, key, value)
        session.add(metadata)
    session.commit()
    session.refresh(metadata)
    return metadata


def delete_ytb_metadata(session: Session, song_id: str) -> bool:
    metadata = get_ytb_metadata(session, song_id)
    if metadata is None:
        return False
    session.delete(metadata)
    session.commit()
    return True