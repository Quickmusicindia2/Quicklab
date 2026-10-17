import asyncio
import json

from app.services.job_queue import pop_job


async def worker_loop():
    while True:
        job = pop_job()
        if job:
            print(f"Processing job: {job['job_id']} -> {job['job_type']}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(worker_loop())
