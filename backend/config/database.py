from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from env_loader import load_env
import os

load_env()


engine = create_engine(url=os.getenv("DATABASE_URL"))
Base = declarative_base()
SesssionLocal = sessionmaker(bind=engine)


