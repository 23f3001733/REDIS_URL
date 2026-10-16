import os
import redis
from fastapi import FastAPI

app = FastAPI()

# Render gives us the Redis address through an environment variable
r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)

@app.post("/hit/{key}")
def hit(key: str):
    count = r.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
def get_count(key: str):
    value = r.get(key)
    return {"key": key, "count": int(value) if value else 0}

@app.get("/healthz")
def healthz():
    try:
        r.ping()
        return {"status": "ok", "redis": "up"}
    except Exception:
        return {"status": "error", "redis": "down"}
