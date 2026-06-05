#!/usr/bin/env python3
"""Télécharge une piste audio YouTube en MP3.

Usage:
  python3 src/main.py <youtube_url>
  python3 src/main.py -c <youtube_url>
  python3 src/main.py --download <video_id>
  python3 src/main.py -c <playlist_url>
  python3 src/main.py --download-playlist <playlist_id>

Le script accepte une URL YouTube en entrée et prépare le téléchargement en MP3.
Il supporte également la préparation et le téléchargement différé de playlists.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from bdd.database import get_engine_from_env, get_session
from bdd.crud import create_or_update_song, is_song_downloaded, mark_song_downloaded

YOUTUBE_URL_RE = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/)?(?P<id>[A-Za-z0-9_-]{11})"
)


def validate_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("URL YouTube vide.")
    if get_playlist_id(url) or YOUTUBE_URL_RE.match(url):
        return url
    raise ValueError("URL YouTube invalide. Exemple: https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def ensure_download_folder(folder: str) -> None:
    os.makedirs(folder, exist_ok=True)


def get_video_id(url: str) -> str:
    match = YOUTUBE_URL_RE.match(url)
    if not match:
        raise ValueError("Impossible de récupérer l'ID vidéo depuis l'URL.")
    return match.group("id")


def get_playlist_id(url: str) -> Optional[str]:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "list" in query and query["list"]:
        return query["list"][0]
    if parsed.path.startswith("/playlist"):
        match = re.search(r"[?&]list=([A-Za-z0-9_-]+)", url)
        if match:
            return match.group(1)
    return None


def estimate_audio_size(info: dict) -> int:
    if info.get("filesize"):
        return int(info["filesize"])
    if info.get("filesize_approx"):
        return int(info["filesize_approx"])

    for fmt in info.get("formats", []):
        if fmt.get("vcodec") == "none":
            size = fmt.get("filesize") or fmt.get("filesize_approx")
            if size:
                return int(size)

    duration = info.get("duration")
    kbps = info.get("tbr") or info.get("abr") or 192
    if duration and kbps:
        return int(duration * float(kbps) * 1000.0 / 8.0)

    return 0


def save_metadata(info: dict, video_folder: str, downloaded: bool = False, SessionLocal=None) -> str:
    os.makedirs(video_folder, exist_ok=True)
    size_bytes = estimate_audio_size(info)
    metadata = {
        "title": info.get("title"),
        "artist": info.get("artist", info.get("uploader", "Unknown")),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "description": info.get("description", ""),
        "url": info.get("original_url") or info.get("webpage_url") or info.get("url"),
        "video_id": info.get("id"),
        "thumbnail": info.get("thumbnail"),
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / (1024 * 1024), 2) if size_bytes else None,
        "downloaded": downloaded,
    }
    metadata_file = os.path.join(video_folder, f"{metadata['video_id']}_metadata.json")
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    if SessionLocal is not None:
        try:
            with get_session(SessionLocal) as session:
                create_or_update_song(session, metadata)
        except Exception as exc:
            print(f"Avertissement DB : impossible de créer/update le son en base : {exc}")

    print(f"Métadonnées sauvegardées: {metadata_file}")
    return metadata_file


def mp3_exists(video_folder: str) -> bool:
    folder = Path(video_folder)
    if not folder.exists():
        return False
    return any(folder.glob("*.mp3"))


def extract_info(url: str, download: bool = False) -> dict:
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        raise RuntimeError(
            "Le module yt_dlp n'est pas installé. Installez-le avec `pip install yt-dlp`"
        )

    ydl_opts = {
        "quiet": False,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=download)


def download_audio(url: str, video_folder: str) -> None:
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        raise RuntimeError(
            "Le module yt_dlp n'est pas installé. Installez-le avec `pip install yt-dlp`"
        )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(video_folder, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_by_id(video_id: str, destination: str, SessionLocal=None) -> None:
    """Télécharge le MP3 d'une vidéo en utilisant son ID."""
    video_folder = os.path.join(destination, video_id)
    metadata_file = os.path.join(video_folder, f"{video_id}_metadata.json")

    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"Pas de métadonnées trouvées pour l'ID: {video_id}")

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    db_checked = False
    if SessionLocal is not None:
        try:
            with get_session(SessionLocal) as session:
                db_checked = True
                if is_song_downloaded(session, video_id):
                    print(f"MP3 déjà marqué téléchargé en base pour {video_id}. Aucun téléchargement nécessaire.")
                    return
        except Exception as exc:
            print(f"Avertissement DB : impossible de vérifier le statut de téléchargement : {exc}")

    if not db_checked and mp3_exists(video_folder):
        print(f"MP3 déjà présent dans {video_folder}. Aucun téléchargement nécessaire.")
        if SessionLocal is not None:
            try:
                with get_session(SessionLocal) as session:
                    mark_song_downloaded(session, video_id, True)
            except Exception as exc:
                print(f"Avertissement DB : impossible de marquer le son téléchargé : {exc}")
        return

    print(f"Téléchargement de: {metadata['title']}")
    download_audio(f"https://www.youtube.com/watch?v={video_id}", video_folder)
    if SessionLocal is not None:
        try:
            with get_session(SessionLocal) as session:
                mark_song_downloaded(session, video_id, True)
        except Exception as exc:
            print(f"Avertissement DB : impossible de marquer le son téléchargé : {exc}")
    print(f"✓ Téléchargement terminé dans: {video_folder}")


def get_playlist_root(destination: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(destination)), "playlists")


def playlist_metadata_path(destination: str, playlist_id: str) -> str:
    return os.path.join(get_playlist_root(destination), playlist_id, "playlist_metadata.json")


def prepare_playlist(url: str, destination: str, SessionLocal=None) -> str:
    info = extract_info(url, download=False)
    playlist_id = get_playlist_id(url)
    if not playlist_id:
        raise ValueError("Impossible de récupérer l'ID de playlist depuis l'URL.")

    playlist_folder = os.path.join(get_playlist_root(destination), playlist_id)
    os.makedirs(playlist_folder, exist_ok=True)

    playlist_info = {
        "playlist_id": playlist_id,
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "uploader_id": info.get("uploader_id"),
        "webpage_url": info.get("webpage_url"),
        "description": info.get("description", ""),
        "entry_count": len(info.get("entries", [])),
        "video_ids": [],
        "videos": [],
        "total_size_mb": 0,
    }

    total_size_bytes = 0
    for entry in info.get("entries", []):
        if not entry:
            continue
        video_id = entry.get("id")
        if not video_id:
            continue
        video_folder = os.path.join(destination, video_id)
        save_metadata(entry, video_folder, downloaded=False, SessionLocal=SessionLocal)

        size_bytes = estimate_audio_size(entry)
        total_size_bytes += size_bytes
        playlist_info["video_ids"].append(video_id)
        playlist_info["videos"].append({
            "video_id": video_id,
            "title": entry.get("title"),
            "duration": entry.get("duration"),
            "uploader": entry.get("uploader"),
            "url": entry.get("webpage_url"),
            "thumbnail": entry.get("thumbnail"),
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2) if size_bytes else None,
        })

    playlist_info["total_size_mb"] = round(total_size_bytes / (1024 * 1024), 2)

    playlist_file = playlist_metadata_path(destination, playlist_id)
    with open(playlist_file, "w", encoding="utf-8") as f:
        json.dump(playlist_info, f, indent=2, ensure_ascii=False)

    print(f"✓ Préparation de la playlist terminée: {playlist_file}")
    print(f"  ID playlist: {playlist_id}")
    print(f"  Titre: {playlist_info['title']}")
    print(f"  Taille totale estimée: {playlist_info['total_size_mb']} MB")
    print(f"  Vidéos: {playlist_info['entry_count']}")
    print(f"\nPour télécharger la playlist, lancez:")
    print(f"  python3 src/main.py --download-playlist {playlist_id}")

    return playlist_id


def download_playlist(playlist_id: str, destination: str, SessionLocal=None) -> None:
    playlist_file = playlist_metadata_path(destination, playlist_id)
    if not os.path.exists(playlist_file):
        raise FileNotFoundError(f"Pas de préparation de playlist trouvée pour l'ID: {playlist_id}")

    with open(playlist_file, "r", encoding="utf-8") as f:
        playlist_info = json.load(f)

    print(f"Téléchargement de la playlist: {playlist_info.get('title')} ({playlist_id})")
    for video in playlist_info.get("videos", []):
        video_id = video.get("video_id")
        if not video_id:
            continue
        try:
            download_by_id(video_id, destination, SessionLocal=SessionLocal)
        except Exception as exc:
            print(f"Erreur lors du téléchargement de {video_id}: {exc}")

    print(f"✓ Téléchargement final de la playlist terminé: {playlist_id}")


def download_with_cli(url: str, destination: str) -> None:
    yt_dlp_exe = shutil.which("yt-dlp") or shutil.which("yt_dlp")
    if not yt_dlp_exe:
        raise RuntimeError(
            "ni yt-dlp ni yt_dlp introuvable dans le PATH. Installez yt-dlp ou ajoutez-le au PATH."
        )

    command = [
        yt_dlp_exe,
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "192K",
        "-o",
        os.path.join(destination, "%(title)s.%(ext)s"),
        url,
    ]

    subprocess.run(command, check=True)


def init_db_session():
    try:
        _, SessionLocal = get_engine_from_env()
        return SessionLocal
    except Exception as exc:
        print(f"Avertissement DB : connexion impossible ({exc}), la base ne sera pas utilisée.")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Prépare un téléchargement YouTube en MP3.")
    parser.add_argument("url", nargs="?", help="URL de la vidéo ou de la playlist YouTube")
    parser.add_argument(
        "--dest",
        default="downloads",
        help="Dossier de destination pour le MP3 (par défaut: downloads)",
    )
    parser.add_argument(
        "-c", "--prepare",
        action="store_true",
        help="Prépare le téléchargement (collecte les métadonnées uniquement)",
    )
    parser.add_argument(
        "--download",
        help="Télécharge le MP3 pour un ID vidéo donné",
    )
    parser.add_argument(
        "--download-playlist",
        help="Télécharge les vidéos d'une playlist préparée par ID",
    )
    args = parser.parse_args()

    ensure_download_folder(args.dest)
    ensure_download_folder(get_playlist_root(args.dest))
    session_local = init_db_session()

    if args.download_playlist:
        try:
            download_playlist(args.download_playlist, args.dest, SessionLocal=session_local)
            return 0
        except FileNotFoundError as exc:
            print(f"Erreur: {exc}")
            return 1
        except Exception as exc:
            print(f"Échec du téléchargement de la playlist: {exc}")
            return 1

    if args.download:
        try:
            download_by_id(args.download, args.dest, SessionLocal=session_local)
            return 0
        except FileNotFoundError as exc:
            print(f"Erreur: {exc}")
            return 1
        except Exception as exc:
            print(f"Échec du téléchargement: {exc}")
            return 1

    try:
        url = args.url or input("Entrez l'URL YouTube : ")
        url = validate_url(url)
    except ValueError as exc:
        print(f"Erreur: {exc}")
        return 1

    playlist_id = get_playlist_id(url)
    if playlist_id:
        if not args.prepare:
            print("Erreur: le téléchargement direct de playlists n'est pas autorisé.")
            print("Utilisez `-c` pour préparer la playlist, puis `--download-playlist <playlist_id>`.")
            return 1
        try:
            prepare_playlist(url, args.dest, SessionLocal=session_local)
            return 0
        except Exception as exc:
            print(f"Erreur lors de la préparation de la playlist: {exc}")
            return 1

    video_id = get_video_id(url)
    video_folder = os.path.join(args.dest, video_id)

    try:
        info = extract_info(url, download=False)
    except Exception as exc:
        print(f"Erreur lors de la récupération des métadonnées: {exc}")
        return 1

    save_metadata(info, video_folder, downloaded=False, SessionLocal=session_local)

    if args.prepare:
        print("Mode préparation activé : le MP3 ne sera pas téléchargé maintenant.")
        return 0

    if mp3_exists(video_folder):
        print(f"MP3 déjà présent dans {video_folder}. Aucun téléchargement nécessaire.")
        if session_local is not None:
            try:
                with get_session(session_local) as session:
                    mark_song_downloaded(session, video_id, True)
            except Exception as exc:
                print(f"Avertissement DB : impossible de marquer le son téléchargé : {exc}")
        return 0

    print(f"Téléchargement de {url} vers {video_folder}...")
    try:
        download_audio(url, video_folder)
        if session_local is not None:
            with get_session(session_local) as session:
                mark_song_downloaded(session, video_id, True)
    except RuntimeError as exc:
        print(f"Erreur: {exc}")
        print("Tentative avec la commande `yt-dlp` si disponible...")
        try:
            download_with_cli(url, video_folder)
            if session_local is not None:
                with get_session(session_local) as session:
                    mark_song_downloaded(session, video_id, True)
        except Exception as cli_exc:
            print(f"Échec du téléchargement: {cli_exc}")
            return 1

    print("Téléchargement terminé. Le fichier MP3 est dans le dossier:", video_folder)
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
