from fastapi import APIRouter,Depends
from backend.dependecies.admin_dependecy import is_admin
from backend.schemas.analysis_schemas import Query
from backend.services.analysis_services import  getreport,chat_assistant
analysis = APIRouter(prefix="/analysis",tags=['analysis'])

@analysis.get('/')
def get_report(is_admin = Depends(is_admin)):
    return getreport(is_admin)

@analysis.post('/chat')
async def ai_chat(data : Query,is_admin=Depends(is_admin)):
    return await chat_assistant(is_admin,data)