from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.projects import PROJECTS

router = APIRouter(prefix="/timeline", tags=["timeline"])


class TimelineClip(BaseModel):
    id: str
    start: float
    end: float
    label: str
    confidence: float = 0.0


class TimelineResponse(BaseModel):
    project_id: str
    clips: list[TimelineClip]


@router.get("/{project_id}")
def get_timeline(project_id: str):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    return TimelineResponse(
        project_id=project_id,
        clips=[
            TimelineClip(id="clip-1", start=0.0, end=3.0, label="intro", confidence=0.94),
            TimelineClip(id="clip-2", start=3.0, end=8.0, label="highlight", confidence=0.91),
            TimelineClip(id="clip-3", start=8.0, end=12.0, label="caption-shot", confidence=0.93),
        ],
    )
