from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.projects import PROJECTS

router = APIRouter(prefix="/captions", tags=["captions"])


class CaptionItem(BaseModel):
    start: float
    end: float
    text: str


@router.get("/{project_id}")
def get_captions(project_id: str):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project_id,
        "captions": [
            CaptionItem(start=0.0, end=2.4, text="Welcome to Quicklab"),
            CaptionItem(start=2.5, end=5.0, text="AI-powered editing starts here"),
            CaptionItem(start=5.1, end=8.0, text="Create your next short in minutes"),
        ],
    }
