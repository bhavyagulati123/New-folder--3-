
run "uv pip install -r requirements.txt"

run "uv run uvicorn main:app --reload" 

on "/limited" refresh too many times !
I have used the token bucket algorithm for rate limiting