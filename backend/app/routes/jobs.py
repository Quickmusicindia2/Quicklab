from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.projects import PROJECTS

router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobRequest(BaseModel):
    job_id: str


@router.get("/{job_id}")
def get_job(job_id: str):
    return {"job_id": job_id, "status": "queued", "result": None}
