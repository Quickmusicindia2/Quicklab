from app.config import settings

import redis

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_task(job_type: str, payload: dict):
    return redis_client.lpush("quicklab:jobs", {"job_type": job_type, "payload": payload})
