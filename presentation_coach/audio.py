from __future__ import annotations

from pathlib import Path


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

