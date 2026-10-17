import json
import os
from typing import Any

import redis

from app.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_job(job_type: str, payload: dict[str, Any]) -> str:
    job_id = payload.get("project_id", "job") + f"-{job_type}"
    redis_client.rpush("quicklab:jobs", json.dumps({"job_id": job_id, "job_type": job_type, "payload": payload}))
    return job_id


def pop_job() -> dict[str, Any] | None:
    raw = redis_client.lpop("quicklab:jobs")
    if not raw:
        return None
    return json.loads(raw)
