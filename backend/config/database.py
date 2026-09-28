from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


engine = create_engine(url=os.getenv("DATABASE_URL"))
Base = declarative_base()
SesssionLocal = sessionmaker(bind=engine)


