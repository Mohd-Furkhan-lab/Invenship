from env_loader import load_env
from sqlalchemy import create_engine
import os

load_env()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing in your .env file")

engine = create_engine(DATABASE_URL)