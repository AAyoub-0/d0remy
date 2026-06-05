from contextlib import contextmanager
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_TEMPLATE = "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"


def load_env_file(env_path: str | Path = None) -> dict[str, str]:
    if env_path is None:
        env_path = Path(__file__).resolve().parents[2] / ".env"
    env_path = Path(env_path)
    if not env_path.exists():
        return {}

    values: dict[str, str] = {}
    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


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


def get_engine_from_env(env_path: str | Path = None):
    env = load_env_file(env_path)
    if not env:
        raise FileNotFoundError("Fichier .env introuvable ou vide")

    user = env.get("DB_USER")
    password = env.get("DB_PASSWORD")
    host = env.get("DB_HOST", "127.0.0.1")
    port = int(env.get("DB_PORT", 3306))
    db = env.get("DB_NAME", "ytb_music")

    if not user or not password:
        raise ValueError("DB_USER et DB_PASSWORD doivent être définis dans .env")

    return get_engine(user=user, password=password, host=host, port=port, db=db)


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
