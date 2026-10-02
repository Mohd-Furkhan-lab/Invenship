from fastapi import APIRouter,Depends
from backend.services.admin_services import getusers,adduser,updaterole,deleteuser
from backend.schemas.admin_schemas import AddUser,UpdateRole
from backend.dependecies.admin_dependecy import is_admin

admin = APIRouter(prefix="/admin",tags=["admin"])

@admin.get('/users')
def get_users(email : str | None = None,is_admin = Depends(is_admin)):
    return getusers(is_admin,email)

@admin.post('/users')
def add_user(data:AddUser,is_admin = Depends(is_admin)):
    return adduser(is_admin,data)

@admin.put('/users/update-role')
def update_user_role(data:UpdateRole,is_admin = Depends(is_admin)):
    return updaterole(is_admin,data)

@admin.delete('/users/{email}')
def delete_user(email,is_admin = Depends(is_admin)):
    return deleteuser(is_admin,email)
