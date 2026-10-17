import subprocess


def export_video(input_path: str, output_path: str, quality: str = "1080p"):
    scale_filter = "scale=1920:1080" if quality == "1080p" else "scale=1280:720"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vf",
        scale_filter,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-c:a",
        "aac",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, output_path
