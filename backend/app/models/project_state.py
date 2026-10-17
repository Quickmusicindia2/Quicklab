from pydantic import BaseModel


class ProjectState(BaseModel):
    id: str
    name: str
    description: str | None = None
    status: str = "created"
    video_path: str | None = None
    timeline: list[dict] = []
    captions: list[dict] = []
    export_url: str | None = None
