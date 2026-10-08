from fastapi import HTTPException
from analytics_engine.main import get_full_analysis
from env_loader import load_env
from google import genai
import time
import os

load_env()


def getreport(is_admin):
    if is_admin:
        report = get_full_analysis()
        if report is None:
            raise HTTPException(500,detail="Internal Server Error")
        return report

client = genai.Client(api_key=os.getenv("llm_key"))

def chat(is_admin, data):
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    models = ["gemini-3.8-flash", "gemini-3.8-flash"]
    last_error = None

    for model in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=data.question
                )
                return {"response": response.text}
            except Exception as e:
                last_error = e
                if "503" in str(e) or "429" in str(e):
                    time.sleep(2 ** attempt)  
                    continue
                raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=503, detail=f"Model busy, try again later: {last_error}")