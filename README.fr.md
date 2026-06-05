# d0remy

`d0remy` est un projet pour télécharger des musiques depuis des URLs YouTube et gérer ces téléchargements localement.

## Objectif

- Télécharger des MP3 à partir d'une URL YouTube
- Préparer et stocker des métadonnées locales
- Gérer les vidéos et playlists de manière structurée
- Fournir une interface locale simple pour l'utilisation

## Fonctionnalités

- Téléchargement direct d'une vidéo en MP3
- Préparation des métadonnées vidéo sans téléchargement
- Préparation et téléchargement différé de playlists
- Stockage des informations dans une structure locale claire
- Support du format MP3 avec `yt-dlp` et `ffmpeg`

## Installation

1. Crée un environnement virtuel :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Installe `ffmpeg` si nécessaire :
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

## Usage

- Télécharger une vidéo directement :
  ```bash
  python3 src/main.py https://www.youtube.com/watch?v=<VIDEO_ID>
  ```

- Préparer une vidéo sans télécharger :
  ```bash
  python3 src/main.py -c https://www.youtube.com/watch?v=<VIDEO_ID>
  ```

- Télécharger par ID après préparation :
  ```bash
  python3 src/main.py --download <VIDEO_ID>
  ```

- Préparer une playlist :
  ```bash
  python3 src/main.py -c https://www.youtube.com/playlist?list=<PLAYLIST_ID>
  ```

- Télécharger une playlist préparée :
  ```bash
  python3 src/main.py --download-playlist <PLAYLIST_ID>
  ```

## Organisation des fichiers

- `downloads/` : dossiers vidéo par `video_id`
- `playlists/` : dossiers playlist par `playlist_id`
- `schema.sql` : schéma SQL pour initialiser la base de données
- `install_mariadb.py` : script d'installation MariaDB et création de l'utilisateur
- `src/main.py` : script principal de téléchargement

## Note

Le projet est réalisé en **vibe coding** : un travail rapide, pragmatique et orienté vers le résultat.
