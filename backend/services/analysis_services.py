from fastapi import HTTPException
from analytics_engine.main import get_full_analysis

def getreport(is_admin):
    if is_admin:
        report = get_full_analysis()
        if report is None:
            raise HTTPException(500,detail="Internal Server Error")
        return report

