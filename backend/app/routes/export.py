from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.projects import PROJECTS
from app.services.export_service import export_video

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
def export_video_request(payload: ExportRequest):
    if payload.project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    input_path = PROJECTS[payload.project_id].get("video_path")
    if not input_path:
        raise HTTPException(status_code=400, detail="No video uploaded yet")

    output_path = f"/tmp/quicklab/exports/{payload.project_id}.{payload.format}"
    ok, result_path = export_video(input_path, output_path, payload.quality)

    return ExportResponse(
        project_id=payload.project_id,
        status="completed" if ok else "failed",
        url=result_path if ok else None,
        message="Export completed successfully." if ok else "Export failed.",
    )
