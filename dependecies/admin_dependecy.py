from auth.token import verify_token
from fastapi import Request,HTTPException

def is_admin(request:Request):
    token = request.cookies.get("access")
    if token is None:
        raise HTTPException(401,detail="Authorization token missing")
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(401,detail="Invalid or expired token")
    if payload.get("role") != "admin":
        raise HTTPException(403,detail="Forbidden Admin only")
    return payload

