from fastapi import FastAPI, Request
from limiting_algorithms import RateLimitExceeded, TokenBucket
app = FastAPI()
ip_addresses = {}

@app.get("/limited")
def limited(request: Request):
    client = request.client.host
    try:
        if client not in ip_addresses:
            ip_addresses[client] = TokenBucket()
        if ip_addresses[client].allow_request():
            return "This is a limited use API"
    except RateLimitExceeded as e:
        raise e

@app.get("/unlimited")
def unlimited(request: Request):
    return "Free to use API limitless"