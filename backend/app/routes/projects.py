from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.routes.projects import PROJECTS
from app.services.ai_service import analyze_video
from app.services.caption_service import generate_captions
from app.services.media_service import save_upload
from app.services.scene_service import detect_scenes

router = APIRouter(prefix="/projects", tags=["projects"])


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

    saved_path = await save_upload(project_id, file)
    project = PROJECTS[project_id]
    project["video_path"] = saved_path
    project["status"] = "analyzing"

    cuts = detect_scenes(saved_path)
    captions = generate_captions(saved_path)
    result = await analyze_video(file)

    return {
        "project_id": project_id,
        "status": "analysis_complete",
        "analysis": {
            **result,
            "scene_count": len(cuts),
            "scene_boundaries": cuts[:10],
            "captions": captions[:10],
        },
    }


@router.get("/{project_id}/captions")
def get_captions(project_id: str):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project_id,
        "captions": [
            {"start": 0.0, "end": 2.4, "text": "Welcome to Quicklab"},
            {"start": 2.5, "end": 5.0, "text": "AI-powered editing starts here"},
            {"start": 5.1, "end": 8.0, "text": "Create your next short in minutes"},
        ],
    }
