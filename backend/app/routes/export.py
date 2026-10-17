from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.projects import PROJECTS

router = APIRouter(prefix="/export", tags=["export"])


class ExportRequest(BaseModel):
    project_id: str
    format: str = "mp4"
    quality: str = "1080p"


class ExportResponse(BaseModel):
    project_id: str
    status: str
    url: str | None = None
    message: str


@router.post("")
def export_video(payload: ExportRequest):
    if payload.project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    return ExportResponse(
        project_id=payload.project_id,
        status="queued",
        url=f"/exports/{payload.project_id}.{payload.format}",
        message=f"Export queued for {payload.project_id} in {payload.format} at {payload.quality}.",
    )
