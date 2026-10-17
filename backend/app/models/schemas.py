from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class JobStatus(BaseModel):
    project_id: str
    job_type: str
    status: str
    result: dict | None = None
    error: str | None = None
