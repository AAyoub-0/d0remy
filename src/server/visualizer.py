"""Génération d'un objet de visualisation audio à partir d'un fichier MP3.

Ce module ne dépend pas de la base de données.
Il renvoie un objet Python prêt à être stocké dans visualizer_data.
"""

import argparse
import json
import math
import struct
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _decode_pcm_samples(mp3_path: Path, sample_rate: int = 22050) -> Tuple[List[int], int]:
    """Décoder un fichier audio en échantillons PCM mono 16-bit via ffmpeg."""
    command = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-i",
        str(mp3_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-f",
        "s16le",
        "-acodec",
        "pcm_s16le",
        "pipe:1",
    ]

    try:
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError as exc:
        raise RuntimeError("ffmpeg est introuvable sur le système.") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Impossible de décoder le fichier audio : {stderr or exc}") from exc

    raw_audio = completed.stdout
    if not raw_audio:
        raise RuntimeError("Aucune donnée audio n'a pu être lue depuis le fichier.")

    if len(raw_audio) % 2 != 0:
        raw_audio = raw_audio[:-1]

    samples = [struct.unpack_from("<h", raw_audio, offset)[0] for offset in range(0, len(raw_audio), 2)]
    if not samples:
        raise RuntimeError("Le fichier audio ne contient aucun échantillon exploitable.")
    return samples, sample_rate


def _get_duration_seconds(mp3_path: Path) -> Optional[float]:
    """Récupérer la durée du fichier via ffprobe si possible."""
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(mp3_path),
    ]
    try:
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    text = completed.stdout.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _resolve_bar_count(duration_seconds: Optional[float], requested_bar_count: Optional[int]) -> int:
    """Déterminer le nombre de barres à générer à partir de la durée du son."""
    if requested_bar_count is not None:
        if requested_bar_count <= 0:
            raise ValueError("bar_count doit être supérieur à 0")
        return requested_bar_count

    if duration_seconds is None or duration_seconds <= 0:
        return 32

    return max(1, int(math.ceil(duration_seconds * 2)))


def _compute_bars(samples: List[int], bar_count: int) -> List[float]:
    """Créer des barres d'intensité à partir des échantillons audio."""
    if bar_count <= 0:
        raise ValueError("bar_count doit être supérieur à 0")

    if not samples:
        return [0.0] * bar_count

    bars: List[float] = []
    chunk_size = max(1, len(samples) // bar_count)
    for index in range(bar_count):
        start = index * chunk_size
        end = start + chunk_size
        chunk = samples[start:end]
        if not chunk:
            bars.append(0.0)
            continue

        rms = math.sqrt(sum((sample / 32768.0) ** 2 for sample in chunk) / len(chunk))
        value = max(0.0, min(1.0, round(rms * 2.5, 3)))
        bars.append(value)

    return bars


def _compute_frequency_levels(samples: List[int], sample_rate: int, frequencies: List[int]) -> List[float]:
    """Calculer des niveaux d'amplitude sur plusieurs bandes de fréquence."""
    if not samples:
        return [0.0] * len(frequencies)

    window_size = min(len(samples), 8192)
    window = samples[:window_size]
    levels: List[float] = []

    for frequency in frequencies:
        if frequency <= 0 or frequency >= sample_rate / 2:
            levels.append(0.0)
            continue

        real = 0.0
        imag = 0.0
        for index, sample in enumerate(window):
            angle = 2 * math.pi * frequency * index / sample_rate
            real += sample * math.cos(angle)
            imag += sample * math.sin(angle)

        magnitude = math.sqrt(real * real + imag * imag) / (window_size * 32768.0)
        normalized = max(0.0, min(1.0, round(magnitude * 10.0, 3)))
        levels.append(normalized)

    return levels


def build_visualizer_data(
    mp3_path: str | Path,
    bar_count: Optional[int] = None,
    frequencies: Optional[List[int]] = None,
) -> Dict[str, object]:
    """Créer un objet de visualisation audio à partir d'un fichier MP3.

    Args:
        mp3_path: chemin du fichier MP3.
        bar_count: nombre de barres à générer. Si absent, une barre est générée par seconde.
        frequencies: liste de fréquences cibles à analyser.

    Returns:
        Un dictionnaire prêt à être sérialisé en JSON.
    """
    audio_path = Path(mp3_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Le fichier audio est introuvable : {audio_path}")
    if not audio_path.is_file():
        raise ValueError(f"Le chemin fourni n'est pas un fichier valide : {audio_path}")

    samples, sample_rate = _decode_pcm_samples(audio_path)
    duration = _get_duration_seconds(audio_path)
    resolved_bar_count = _resolve_bar_count(duration, bar_count)

    if frequencies is None:
        frequencies = [60, 170, 330, 1000, 2000, 4000]

    bars = _compute_bars(samples, resolved_bar_count)
    peak = max(abs(sample) / 32768.0 for sample in samples)
    rms = math.sqrt(sum((sample / 32768.0) ** 2 for sample in samples) / len(samples))
    energy = sum(abs(sample) / 32768.0 for sample in samples) / len(samples)
    frequency_levels = _compute_frequency_levels(samples, sample_rate, frequencies)

    return {
        "bars": bars,
        "bar_count": len(bars),
        "energy": round(energy, 3),
        "peak": round(peak, 3),
        "rms": round(rms, 3),
        "frequencies": frequencies,
        "frequency_levels": frequency_levels,
        "duration_seconds": round(duration, 3) if duration is not None else None,
        "source_file": str(audio_path),
    }


def build_visualizer_json(
    mp3_path: str | Path,
    bar_count: Optional[int] = None,
    frequencies: Optional[List[int]] = None,
) -> str:
    """Retourne une version JSON sérialisée de l'objet visualizer_data."""
    return json.dumps(
        build_visualizer_data(mp3_path, bar_count=bar_count, frequencies=frequencies),
        indent=2,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Génère un objet de visualisation audio à partir d'un fichier MP3")
    parser.add_argument("mp3_path", help="Chemin du fichier MP3 à analyser")
    parser.add_argument("--bar-count", type=int, default=None, help="Nombre de barres à générer (par défaut : une barre par seconde)")
    args = parser.parse_args()

    try:
        print(build_visualizer_json(args.mp3_path, bar_count=args.bar_count))
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Erreur: {exc}")
        raise SystemExit(1)
