import asyncio
from typing import Any

from fastapi import UploadFile


async def analyze_video(file: UploadFile) -> dict[str, Any]:
    await asyncio.sleep(0.2)

    filename = file.filename or "video"
    return {
        "filename": filename,
        "scene_count": 3,
        "suggested_cuts": [
            {"start": 0, "end": 3, "label": "intro"},
            {"start": 3, "end": 8, "label": "highlight"},
            {"start": 8, "end": 12, "label": "caption-shot"},
        ],
        "captions": [
            {"start": 0.0, "end": 2.4, "text": "Welcome to Quicklab"},
            {"start": 2.5, "end": 5.0, "text": "AI-powered editing starts here"},
            {"start": 5.1, "end": 8.0, "text": "Create your next short in minutes"},
        ],
        "ai_summary": "This clip is strong for a short-form edit with an intro hook and clear caption coverage.",
    }
