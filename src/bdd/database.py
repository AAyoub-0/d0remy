from contextlib import contextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_TEMPLATE = "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"


def build_database_url(user: str, password: str, host: str = "127.0.0.1", port: int = 3306, db: str = "ytb_music") -> str:
    password_enc = quote_plus(password)
    return DATABASE_URL_TEMPLATE.format(user=user, password=password_enc, host=host, port=port, db=db)


def create_engine_and_session(database_url: str):
    engine = create_engine(database_url, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return engine, SessionLocal


def get_engine(user: str = None, password: str = None, host: str = "127.0.0.1", port: int = 3306, db: str = "ytb_music", database_url: str = None):
    if database_url is None:
        if user is None or password is None:
            raise ValueError("user and password are required when database_url is not provided")
        database_url = build_database_url(user, password, host, port, db)
    return create_engine_and_session(database_url)


@contextmanager
def get_session(SessionLocal):
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
