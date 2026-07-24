from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ClassificationBase(BaseModel):
    genre: Optional[str] = None
    subgenres: Optional[list[str]] = None
    moods: Optional[list[str]] = None
    language: Optional[str] = None
    is_explicit: Optional[bool] = False


class ClassificationCreate(ClassificationBase):
    pass


class ClassificationUpdate(BaseModel):
    genre: Optional[str] = None
    subgenres: Optional[list[str]] = None
    moods: Optional[list[str]] = None
    language: Optional[str] = None
    is_explicit: Optional[bool] = None


class ClassificationRead(ClassificationBase):
    classification_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True