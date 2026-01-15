from fastapi import FastAPI, Request, HTTPException
from limiting_algorithms import TokenBucket, RateLimitExceeded

app = FastAPI()
bucket = TokenBucket()   # Redis-backed, shared

@app.get("/limited")
def limited(request: Request):
    ip = request.client.host

    try:
        bucket.allow_request(ip)
        return "This is a limited use API"
    except RateLimitExceeded as e:
        raise e

@app.get("/unlimited")
def unlimited():
    return "Free to use API limitless"
