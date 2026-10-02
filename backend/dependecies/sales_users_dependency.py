from fastapi import HTTPException,Request
from backend.auth.token import verify_token

def require_admin_or_receptionist(request : Request):
    token = request.cookies.get("access")
    if token is None:
        raise HTTPException(401,detail="Authorization Token Missing")
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(401,detail="Authorization Token Missing")
    if payload.get("role") not in ["admin","receptionist"]:
        raise HTTPException(403,detail="Forbidden Not Allowed")
    return payload