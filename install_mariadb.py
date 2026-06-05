#!/usr/bin/env python3
"""Installe MariaDB, crée la base via schema.sql et un utilisateur avec droits lecture/écriture."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from src.server.database import get_engine_from_env, get_session

DEFAULT_DB_NAME = "ytb_music"
DEFAULT_SQL_FILE = Path("schema.sql")
DEFAULT_DB_USER = "ytb_user"
DEFAULT_DB_PASSWORD = "ytb_pass"


def run_command(command, check=True):
    print(f"Exécution: {' '.join(command)}")
    subprocess.run(command, check=check)


def is_root():
    return os.geteuid() == 0


def install_mariadb(privilege_prefix):
    run_command(privilege_prefix + ["apt", "update"])
    run_command(privilege_prefix + ["apt", "install", "-y", "mariadb-server", "mariadb-client"])
    run_command(privilege_prefix + ["systemctl", "enable", "--now", "mariadb"])
    run_command(privilege_prefix + ["systemctl", "is-active", "--quiet", "mariadb"])
    print("MariaDB installé et démarré.")


def execute_sql_file(privilege_prefix, sql_file: Path):
    sql_path = sql_file.resolve()
    if not sql_path.exists():
        raise FileNotFoundError(f"Fichier SQL introuvable: {sql_path}")

    run_command(privilege_prefix + ["mysql", "-e", f"source {sql_path}"])
    print(f"Script SQL exécuté: {sql_path}")


def create_database_user(privilege_prefix, db_name: str, user: str, password: str):
    sql = (
        f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        f"CREATE USER IF NOT EXISTS '{user}'@'localhost' IDENTIFIED BY '{password}';"
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON `{db_name}`.* TO '{user}'@'localhost';"
        f"FLUSH PRIVILEGES;"
    )
    run_command(privilege_prefix + ["mysql", "-e", sql])
    print(f"Utilisateur créé: {user}@localhost")
    print(f"Privilèges accordés sur la base: {db_name}")


def main():
    parser = argparse.ArgumentParser(description="Installer MariaDB et initialiser la base de données depuis schema.sql.")
    parser.add_argument("--db-name", default=DEFAULT_DB_NAME, help="Nom de la base de données")
    parser.add_argument("--sql-file", default=str(DEFAULT_SQL_FILE), help="Chemin vers le fichier SQL de création")
    parser.add_argument("--db-user", default=DEFAULT_DB_USER, help="Nom du compte MariaDB à créer")
    parser.add_argument("--db-password", default=DEFAULT_DB_PASSWORD, help="Mot de passe du compte MariaDB")
    parser.add_argument("--no-install", action="store_true", help="Ne pas installer MariaDB, uniquement exécuter le script SQL et créer l'utilisateur")
    args = parser.parse_args()

    privilege_prefix = [] if is_root() else ["sudo"]

    if not args.no_install:
        install_mariadb(privilege_prefix)

    execute_sql_file(privilege_prefix, Path(args.sql_file))
    create_database_user(privilege_prefix, args.db_name, args.db_user, args.db_password)

    print("Installation terminée.")
    print("Connexion MariaDB:")
    print(f"  mysql -u {args.db_user} -p -D {args.db_name}")


if __name__ == "__main__":
    main()
