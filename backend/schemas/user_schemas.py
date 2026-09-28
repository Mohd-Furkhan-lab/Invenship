from pydantic import BaseModel,EmailStr

class Login(BaseModel):
    email : EmailStr
    password : str

class NewPassword(BaseModel):
    oldpassword : str
    newpassword : str