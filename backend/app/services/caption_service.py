import whisper

_model = None


def get_model(model_name: str = "base"):
    global _model
    if _model is None:
        _model = whisper.load_model(model_name)
    return _model


def generate_captions(video_path: str):
    model = get_model("base")
    result = model.transcribe(video_path, fp16=False)
    captions = []
    for segment in result.get("segments", []):
        captions.append({
            "start": segment.get("start", 0.0),
            "end": segment.get("end", 0.0),
            "text": segment.get("text", "").strip(),
        })
    return captions
