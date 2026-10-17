# Quicklab Architecture

Quicklab is an open-source AI video editor with a mobile-first experience and a cloud-capable AI pipeline.

## Core components
- `android/` — Android app shell for editing and export
- `backend/` — API and media processing orchestration
- `tools/` — scripts for local setup and model download
- `docs/` — architecture and onboarding notes

## Processing flow
1. User imports media from the gallery or camera
2. Android app previews the media
3. Backend stores project metadata and media references
4. AI workers analyze clips for scenes, captions, and highlights
5. Editor surfaces suggested cuts, subtitles, and effects
6. User exports final render to MP4

## AI tasks supported in early milestones
- Scene detection
- Automatic cut suggestions
- Whisper-based captions
- Background blur / object masking
- Template-based auto-editing

## Open-source direction
Quicklab intentionally uses open-source libraries and model families that are accessible for community building and educational use. However, some model weights may have separate licenses, so contributors must review those model cards before use.
