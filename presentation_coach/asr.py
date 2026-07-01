from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
from transformers import pipeline


DEFAULT_MODEL_ID = "vinai/PhoWhisper-base"


@lru_cache(maxsize=1)
def load_asr_pipeline(model_id: str = DEFAULT_MODEL_ID):
    device = 0 if torch.cuda.is_available() else -1
    kwargs = {
        "model": model_id,
        "device": device,
        "chunk_length_s": 30,
        "batch_size": 1,
    }
    if device == 0:
        kwargs["torch_dtype"] = torch.float16

    return pipeline("automatic-speech-recognition", **kwargs)


def transcribe_audio(audio_path: str | Path, model_id: str = DEFAULT_MODEL_ID) -> str:
    asr_pipeline = load_asr_pipeline(model_id)
    path = str(audio_path)

    try:
        result = asr_pipeline(
            path,
            generate_kwargs={"language": "vi", "task": "transcribe"},
        )
    except (TypeError, ValueError):
        result = asr_pipeline(path)

    if isinstance(result, dict):
        return result.get("text", "").strip()
    return str(result).strip()
