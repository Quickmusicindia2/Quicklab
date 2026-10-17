from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.projects import PROJECTS

router = APIRouter(prefix="/projects", tags=["projects"])


class PersistRequest(BaseModel):
    project_id: str
    timeline: list[dict] = []
    captions: list[dict] = []


@router.post("/{project_id}/persist")
def persist_project(project_id: str, payload: PersistRequest):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    PROJECTS[project_id]["timeline"] = payload.timeline
    PROJECTS[project_id]["captions"] = payload.captions
    return {
        "project_id": project_id,
        "status": "saved",
        "timeline_count": len(payload.timeline),
        "caption_count": len(payload.captions),
    }
