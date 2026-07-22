#!/usr/bin/env python3
"""Generate visualizer_data for songs stored in the database.

This script scans songs from DB, locates each MP3 file in downloads/<video_id>/,
generates visualizer_data from audio, and stores it in songs.visualizer_data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from sqlalchemy.orm import Session

# Allow running the script directly with `python3 src/server/generate_visualizers.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.server.database import Song, get_engine_from_env
from src.server.visualizer import build_visualizer_data


def _has_visualizer_data(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    bars = value.get("bars")
    return isinstance(bars, list) and len(bars) > 0


def _find_mp3(downloads_dir: Path, video_id: str) -> Path | None:
    song_dir = downloads_dir / video_id
    if not song_dir.exists() or not song_dir.is_dir():
        return None

    mp3_files = sorted(song_dir.glob("*.mp3"))
    if not mp3_files:
        return None
    return mp3_files[0]


def _update_metadata_file(song_dir: Path, video_id: str, visualizer_data: dict[str, Any]) -> None:
    metadata_path = song_dir / f"{video_id}_metadata.json"
    if not metadata_path.exists() or not metadata_path.is_file():
        return

    try:
        with metadata_path.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
    except (OSError, json.JSONDecodeError):
        return

    metadata["visualizer_data"] = visualizer_data
    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def _process_song(
    session: Session,
    song: Song,
    downloads_dir: Path,
    force: bool,
    bar_count: int | None,
) -> tuple[bool, str]:
    if not force and _has_visualizer_data(song.visualizer_data):
        return False, "skip: visualizer_data already set"

    mp3_path = _find_mp3(downloads_dir, song.video_id)
    if mp3_path is None:
        return False, "skip: no mp3 found"

    visualizer_data = build_visualizer_data(mp3_path, bar_count=bar_count)
    song.visualizer_data = visualizer_data
    session.add(song)
    session.commit()

    _update_metadata_file(mp3_path.parent, song.video_id, visualizer_data)
    return True, f"ok: {mp3_path.name}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate visualizer_data for songs in DB")
    parser.add_argument(
        "--downloads-dir",
        default="downloads",
        help="Base directory that contains one folder per video_id (default: downloads)",
    )
    parser.add_argument(
        "--video-id",
        default=None,
        help="Only process one song by video_id",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recompute visualizer_data even when already present",
    )
    parser.add_argument(
        "--bar-count",
        type=int,
        default=None,
        help="Override number of bars",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Path to .env file (optional)",
    )
    args = parser.parse_args()

    downloads_dir = Path(args.downloads_dir).resolve()
    if not downloads_dir.exists() or not downloads_dir.is_dir():
        print(f"Error: downloads dir not found: {downloads_dir}")
        return 1

    try:
        _, SessionLocal = get_engine_from_env(args.env_file)
    except Exception as exc:
        print(f"Error: DB connection failed: {exc}")
        return 1

    updated = 0
    skipped = 0
    failed = 0

    session = SessionLocal()
    try:
        query = session.query(Song)
        if args.video_id:
            query = query.filter(Song.video_id == args.video_id)

        songs = query.all()
        if not songs:
            if args.video_id:
                print(f"No song found for video_id={args.video_id}")
            else:
                print("No songs found in DB")
            return 0

        for song in songs:
            try:
                is_updated, message = _process_song(
                    session=session,
                    song=song,
                    downloads_dir=downloads_dir,
                    force=args.force,
                    bar_count=args.bar_count,
                )
                if is_updated:
                    updated += 1
                else:
                    skipped += 1
                print(f"[{song.video_id}] {message}")
            except Exception as exc:
                session.rollback()
                failed += 1
                print(f"[{song.video_id}] fail: {exc}")

    finally:
        session.close()

    print("---")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")

    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
