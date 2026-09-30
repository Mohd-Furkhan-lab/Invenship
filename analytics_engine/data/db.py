from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

databaseurl = os.getenv("DATABASE_URL")


engine = create_engine(databaseurl)

