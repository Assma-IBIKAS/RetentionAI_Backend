from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os

USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

DATABASE_URL = f"postgresql://{USER_DB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine= create_engine(DATABASE_URL)

sessionLocal= sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def getdb():
    db = sessionLocal()     
    try:
      yield db
    finally:
      db.close()