from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import ClassificationCreate, ClassificationRead, ClassificationUpdate
from ...database.repositories.classification_repository import create_classification, get_classification, list_classifications

router = APIRouter(prefix="/classifications", tags=["classifications"])


@router.get("", response_model=List[ClassificationRead])
def read_classifications(db: Session = Depends(get_db)):
    return list_classifications(db)


@router.post("", response_model=ClassificationRead, status_code=201)
def create_classification_endpoint(classification: ClassificationCreate, db: Session = Depends(get_db)):
    return create_classification(db, classification.dict())


@router.get("/{classification_id}", response_model=ClassificationRead)
def read_classification(classification_id: int, db: Session = Depends(get_db)):
    classification = get_classification(db, classification_id)
    if classification is None:
        raise HTTPException(status_code=404, detail="Classification introuvable")
    return classification


@router.put("/{classification_id}", response_model=ClassificationRead)
def update_classification(classification_id: int, classification_update: ClassificationUpdate, db: Session = Depends(get_db)):
    classification = get_classification(db, classification_id)
    if classification is None:
        raise HTTPException(status_code=404, detail="Classification introuvable")
    for key, value in classification_update.dict(exclude_unset=True).items():
        setattr(classification, key, value)
    db.add(classification)
    db.commit()
    db.refresh(classification)
    return classification


@router.delete("/{classification_id}", status_code=204)
def delete_classification(classification_id: int, db: Session = Depends(get_db)):
    classification = get_classification(db, classification_id)
    if classification is None:
        raise HTTPException(status_code=404, detail="Classification introuvable")
    db.delete(classification)
    db.commit()