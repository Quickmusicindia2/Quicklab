import os
import time
from pathlib import Path

from app.services.whisper_service import transcribe_video


def benchmark_whisper(video_path: str, model_name: str = "tiny"):
    start = time.time()
    captions = transcribe_video(video_path, model_name=model_name)
    elapsed = time.time() - start
    return {
        "model": model_name,
        "duration_seconds": round(elapsed, 2),
        "captions_count": len(captions),
        "sample": captions[:3],
    }
