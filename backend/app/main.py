from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.captions import router as captions_router
from app.routes.export import router as export_router
from app.routes.projects import router as projects_router
from app.routes.timeline import router as timeline_router

app = FastAPI(
    title="Quicklab",
    version="0.1.0",
    description="Open-source AI video editor backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router, prefix="/api/v1")
app.include_router(timeline_router, prefix="/api/v1")
app.include_router(captions_router, prefix="/api/v1")
app.include_router(export_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "quicklab-backend"}


@app.get("/")
def root():
    return {"message": "Welcome to Quicklab API"}
