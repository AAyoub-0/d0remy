from sqlalchemy.orm import Session

from ..entities.models import Classification


def create_classification(session: Session, classification_data: dict) -> Classification:
    classification = Classification(**classification_data)
    session.add(classification)
    session.commit()
    session.refresh(classification)
    return classification


def get_classification(session: Session, classification_id: int) -> Classification | None:
    return session.get(Classification, classification_id)


def list_classifications(session: Session, limit: int = 100) -> list[Classification]:
    return session.query(Classification).limit(limit).all()