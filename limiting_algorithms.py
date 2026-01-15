import time
import redis
from fastapi import HTTPException

r = redis.Redis(host="redis", port=6379, decode_responses=True)

class RateLimitExceeded(HTTPException):
    def __init__(self, detail="Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)

class TokenBucket:
    def __init__(self):
        self.capacity = 10
        self.refill_rate = 1  # tokens per second

    def allow_request(self, ip: str):
        now = time.time()
        key = f"bucket:{ip}"

        # Get last state
        data = r.hmget(key, "tokens", "last")

        tokens = float(data[0]) if data[0] else self.capacity
        last = float(data[1]) if data[1] else now

        # Refill tokens
        delta = now - last
        tokens = min(self.capacity, tokens + delta * self.refill_rate)

        if tokens < 1:
            raise RateLimitExceeded()

        # Consume token
        tokens -= 1

        # Save back to Redis
        r.hset(key, mapping={"tokens": tokens, "last": now})
        r.expire(key, 60)

        return True
