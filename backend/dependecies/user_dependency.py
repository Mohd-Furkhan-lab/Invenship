from fastapi import Request,HTTPException
from backend.auth.token import verify_token

def get_access_payload(request:Request):
    token = request.cookies.get("access")
    if token is None:
        raise HTTPException(401,detail="Authorization token missing")
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(401,detail="Invalid or expired token")
    return payload

def get_refresh_payload(request:Request):
    token = request.cookies.get("refresh")
    if token is None:
        raise HTTPException(401,detail="Authorization token missing")
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(401,detail="Invalid or expired token")
    return payload