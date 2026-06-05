from .database import get_engine
from .entities.models import Base


def create_tables(user: str, password: str, host: str = "127.0.0.1", port: int = 3306, db: str = "ytb_music"):
    engine, _ = get_engine(user=user, password=password, host=host, port=port, db=db)
    Base.metadata.create_all(engine)
    print(f"Tables créées dans la base {db}.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Créer les tables SQLAlchemy dans MariaDB.")
    parser.add_argument("--user", required=True, help="Utilisateur MariaDB")
    parser.add_argument("--password", required=True, help="Mot de passe MariaDB")
    parser.add_argument("--host", default="127.0.0.1", help="Hôte MariaDB")
    parser.add_argument("--port", type=int, default=3306, help="Port MariaDB")
    parser.add_argument("--db", default="ytb_music", help="Nom de la base de données")
    args = parser.parse_args()

    create_tables(args.user, args.password, args.host, args.port, args.db)
