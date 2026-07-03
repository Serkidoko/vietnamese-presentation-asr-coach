from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


FFMPEG_MISSING_HINT = (
    "FFmpeg is required to read this audio file. Install it with "
    "`conda install -c conda-forge ffmpeg -y`, then restart the app."
)


def convert_audio_to_wav(
    audio_path: str | Path,
    sample_rate: int = 16000,
) -> Path:
    source_path = Path(audio_path)
    fd, output_name = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    output_path = Path(output_name)

    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(source_path),
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-vn",
        str(output_path),
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        output_path.unlink(missing_ok=True)
        raise RuntimeError(FFMPEG_MISSING_HINT) from exc
    except subprocess.CalledProcessError as exc:
        output_path.unlink(missing_ok=True)
        detail = exc.stderr.strip() or "unknown ffmpeg error"
        raise RuntimeError(f"Could not convert audio file with FFmpeg: {detail}") from exc

    return output_path


def get_audio_duration_seconds(audio_path: str | Path) -> float:
    path = str(audio_path)

    try:
        import soundfile as sf

        info = sf.info(path)
        return float(info.frames / info.samplerate)
    except Exception:
        pass

    try:
        import librosa

        audio, sample_rate = librosa.load(path, sr=None, mono=True)
        return float(len(audio) / sample_rate)
    except Exception as exc:
        raise RuntimeError(f"Could not read audio duration from {path}") from exc
