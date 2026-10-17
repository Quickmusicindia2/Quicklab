from pathlib import Path
import subprocess


def detect_scenes(video_path: str):
    output_dir = Path("/tmp/quicklab/scenes")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            "scenedetect",
            "--input",
            video_path,
            "--output",
            str(output_dir),
            "detect-content",
            "list-scenes",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    cuts = []
    for line in result.stdout.splitlines():
        if "seconds" in line.lower() or "Scene" in line:
            cuts.append(line.strip())
    return cuts
