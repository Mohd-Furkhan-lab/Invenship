from pydantic import BaseModel

class AddUser(BaseModel):
    name : str
    email : str
    password : str
    role : str

class UpdateRole(BaseModel):
    email : str
    new_role : str