# database_setup.py

from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Define server and database information
server_name = os.getenv('SERVER_NAME', 'default_server')
database = os.getenv('DATABASE_NAME', 'default_database')
username = os.getenv('DB_USERNAME', 'default_username')
password = os.getenv('DB_PASSWORD', 'default_password')
driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')

# Create the database engine
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server_name}/{database}?driver={driver}')
Session = sessionmaker(bind=engine)
Base = declarative_base()





class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create tables
def create_tables():
    Base.metadata.create_all(engine)
