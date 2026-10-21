from fastapi import APIRouter,Depends
from backend.dependecies.admin_dependecy import is_admin
from backend.services.analysis_services import  getreport
analysis = APIRouter(prefix="/analysis",tags=['analysis'])

@analysis.get('/')
def get_report(is_admin = Depends(is_admin)):
    return getreport(is_admin)
