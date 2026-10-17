from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.ai_service import analyze_video
from app.services.media_service import save_upload

router = APIRouter(prefix="/projects", tags=["projects"])

PROJECTS: dict[str, dict] = {}


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None


@router.get("")
def list_projects():
    return {"projects": list(PROJECTS.values())}


@router.post("")
def create_project(payload: ProjectCreateRequest):
    project_id = f"proj-{len(PROJECTS) + 1:04d}"
    project = {
        "id": project_id,
        "name": payload.name,
        "description": payload.description,
        "status": "created",
        "video_path": None,
    }
    PROJECTS[project_id] = project
    return project


@router.post("/{project_id}/upload")
async def upload_video(project_id: str, file: UploadFile = File(...)):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    saved_path = await save_upload(project_id, file)
    PROJECTS[project_id]["video_path"] = saved_path
    PROJECTS[project_id]["status"] = "uploaded"

    return {
        "project_id": project_id,
        "filename": file.filename,
        "saved_path": saved_path,
        "status": "uploaded",
    }


@router.post("/{project_id}/analyze")
async def analyze_project_video(project_id: str, file: UploadFile = File(...)):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await analyze_video(file)
    return {
        "project_id": project_id,
        "status": "analysis_complete",
        "analysis": result,
    }
