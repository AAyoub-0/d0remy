.PHONY: help venv install setup run-api mariadb ffmpeg clean

help:
	@echo "Commandes disponibles:"
	@echo "  make venv         - Créer l'environnement virtuel"
	@echo "  make install      - Installer les requirements"
	@echo "  make ffmpeg       - Installer ffmpeg (nécessite sudo)"
	@echo "  make setup        - Créer venv, installer requirements et ffmpeg"
	@echo "  make run-api      - Lancer l'API FastAPI"
	@echo "  make mariadb      - Installer MariaDB (nécessite sudo)"
	@echo "  make clean        - Supprimer venv et fichiers temporaires"

venv:
	python3 -m venv venv

install:
	. venv/bin/activate && python3 -m pip install -r requirements.txt

ffmpeg:
	@command -v ffmpeg >/dev/null 2>&1 && \
		echo "ffmpeg déjà installé" || \
		(sudo apt-get update && sudo apt-get install -y ffmpeg)

setup: venv install ffmpeg

run-api:
	. venv/bin/activate && python3 -m uvicorn src.server.api.app:app --reload

mariadb:
	sudo python3 install_mariadb.py

clean:
	rm -rf venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
