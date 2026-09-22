from fastapi import APIRouter,Depends,Response
from dependecies.user_dependency import get_access_payload,get_refresh_payload
from services.user_services import getinfo,refreshtoken,userlogin,userlogout,changepassword
from schemas.user_schemas import Login,NewPassword
users = APIRouter(prefix="/users",tags=["users"])


@users.post('/login')
def login(response:Response,data:Login):
    atoken,rtoken = userlogin(data)
    response.set_cookie(
        key="access",
        value=atoken,
        secure=False,
        httponly=True
    )
    response.set_cookie(
            key="refresh",
            value=rtoken,
            secure=False,
            httponly=True
        )
    return {"message" : "login successfully"}

@users.post('/logout')
def logout(reponse:Response,access= Depends(get_access_payload),refreh = Depends(get_refresh_payload)):
    reponse.delete_cookie("access")
    reponse.delete_cookie("refresh")
    return userlogout(refreh,access)

@users.post('/refresh')
def refresh_token(response:Response,payload = Depends(get_refresh_payload)):
    token = refreshtoken(payload)
    response.set_cookie(
            key="access",
            value=token,
            secure=False,
            httponly=True
        )
    return {"message" : "token refreshed"}

@users.put('/new-password')
def change_password(data:NewPassword,payload = Depends(get_access_payload)):
    return changepassword(data,payload)

@users.get('/me')
def my_details(payload = Depends(get_access_payload)):
    return getinfo(payload)