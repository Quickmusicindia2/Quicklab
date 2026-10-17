import os
from pathlib import Path

from fastapi import UploadFile


async def save_upload(project_id: str, file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("Filename is required")

    allowed = {"mp4", "mov", "mkv", "avi", "webm"}
    suffix = Path(file.filename).suffix.lower().lstrip(".")
    if suffix not in allowed:
        raise ValueError(f"Unsupported video type: {suffix}")

    base_dir = Path("/tmp/quicklab") / project_id
    base_dir.mkdir(parents=True, exist_ok=True)
    target_path = base_dir / file.filename

    content = await file.read()
    target_path.write_bytes(content)
    return str(target_path)
