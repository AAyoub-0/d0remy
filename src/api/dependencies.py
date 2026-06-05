from typing import Generator

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..bdd.database import get_engine_from_env, get_session

try:
    engine, SessionLocal = get_engine_from_env()
except Exception as exc:
    SessionLocal = None
    print(f"Avertissement API DB : {exc}")


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise HTTPException(status_code=500, detail="Database configuration introuvable")
    with get_session(SessionLocal) as session:
        yield session
