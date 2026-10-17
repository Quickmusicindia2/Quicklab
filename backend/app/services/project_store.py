from app.routes.projects import PROJECTS


def save_project_state(project_id: str, payload: dict):
    project = PROJECTS.setdefault(project_id, {})
    project.update(payload)


def get_project_state(project_id: str):
    if project_id not in PROJECTS:
        return None
    return PROJECTS[project_id]
