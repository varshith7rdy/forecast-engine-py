from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, pool_size=5, max_overflow=10)

def get_db_engine():
    return engine