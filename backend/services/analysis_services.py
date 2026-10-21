from fastapi import HTTPException
from analytics_engine.main import get_full_analysis
from env_loader import load_env
from ollama import Client
from fastmcp import Client as McpClient
import os

load_env()



def getreport(is_admin):
    if is_admin:
        report = get_full_analysis()
        if report is None:
            raise HTTPException(500,detail="Internal Server Error")
        return report
