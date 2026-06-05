# d0remy

`d0remy` is a project for downloading music from YouTube URLs and managing downloads locally.

## Purpose

- Download MP3 files from YouTube videos
- Prepare and store local metadata
- Manage videos and playlists in a structured way
- Provide a simple local interface for usage

## Features

- Direct download of a video to MP3
- Metadata-only preparation without downloading
- Deferred playlist preparation and download
- Clean local storage structure
- MP3 support using `yt-dlp` and `ffmpeg`

## Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install `ffmpeg` if needed:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

## Usage

- Download a video directly:
  ```bash
  python3 src/main.py https://www.youtube.com/watch?v=<VIDEO_ID>
  ```

- Prepare a video without downloading:
  ```bash
  python3 src/main.py -c https://www.youtube.com/watch?v=<VIDEO_ID>
  ```

- Download by ID after preparation:
  ```bash
  python3 src/main.py --download <VIDEO_ID>
  ```

- Prepare a playlist:
  ```bash
  python3 src/main.py -c https://www.youtube.com/playlist?list=<PLAYLIST_ID>
  ```

- Download a prepared playlist:
  ```bash
  python3 src/main.py --download-playlist <PLAYLIST_ID>
  ```

## File structure

- `downloads/` : video folders by `video_id`
- `playlists/` : playlist folders by `playlist_id`
- `schema.sql` : SQL schema for database initialization
- `install_mariadb.py` : script to install MariaDB and create the database user
- `src/main.py` : main download script

## Note

This project is built in a **vibe coding** style: fast, pragmatic, and results-oriented.
