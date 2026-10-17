import os
from pathlib import Path

import torch
import whisper

from app.config import settings

_MODEL_CACHE_DIR = Path(os.getenv("WHISPER_CACHE_DIR", "/tmp/whisper-models"))
_MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_model_name() -> str:
    model_name = os.getenv("QUICKLAB_WHISPER_MODEL", settings.whisper_model)
    return model_name if model_name in {"tiny", "base", "small", "medium"} else "tiny"


def ensure_model_downloaded(model_name: str) -> str:
    model_path = _MODEL_CACHE_DIR / model_name
    if not model_path.exists():
        model_path.mkdir(parents=True, exist_ok=True)
    return str(model_path)


def load_whisper_model(model_name: str | None = None):
    resolved_name = get_model_name() if model_name is None else model_name
    ensure_model_downloaded(resolved_name)
    return whisper.load_model(resolved_name)


def transcribe_video(video_path: str, model_name: str | None = None):
    model = load_whisper_model(model_name)
    result = model.transcribe(video_path, fp16=torch.cuda.is_available())
    captions = []
    for segment in result.get("segments", []):
        captions.append({
            "start": segment.get("start", 0.0),
            "end": segment.get("end", 0.0),
            "text": segment.get("text", "").strip(),
        })
    return captions
