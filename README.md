# Quicklab

Quicklab is an open-source AI video editor designed for Android-first workflows, with a modular cloud AI pipeline for heavy editing tasks.

## Goals
- Open-source timeline editor for short-form video
- AI-powered captions and auto-edit suggestions
- Fast local preview/editing with cloud AI support
- Simple setup for contributors and hackers

## Stack
- Android app: Kotlin + Jetpack Compose
- Backend: FastAPI + Python
- Media pipeline: FFmpeg + OpenCV
- AI: Whisper, scene detection, YOLO, segmentation models
- Storage: MinIO/S3-compatible object storage
- Dev runtime: Docker + Docker Compose

## Repository layout
- `android/` — starter Android app scaffold
- `backend/` — FastAPI API and AI worker skeleton
- `docs/` — architecture and contributor notes
- `tools/` — scripts for setup and model downloads
- `docker-compose.yml` — local dev stack

## Quick start

### 1) Clone the repo
```bash
git clone https://github.com/Quickmusicindia2/Quicklab.git
cd Quicklab
```

### 2) Start local services
```bash
docker compose up --build
```

### 3) Backend health check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok","service":"quicklab-backend"}
```

## Roadmap
- Basic timeline and trimming
- Auto captions
- Smart cut suggestions
- Background blur / replacement
- AI assistant for prompt-driven edits
- Android export workflow

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License
This project is licensed under the Apache License 2.0.
