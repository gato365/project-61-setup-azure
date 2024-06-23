import os
from dotenv import load_dotenv

# Import the necessary libraries
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




load_dotenv()

# Define server and database information
server_name = os.getenv('SERVER_NAME', 'default_server')
database = os.getenv('DATABASE_NAME', 'default_database')
username = os.getenv('DB_USERNAME', 'default_username')
password = os.getenv('DB_PASSWORD', 'default_password')
driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')


# Create the database engine for SQL Server
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server_name}/{database}?driver={driver}')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Add some mock data
user1 = User(name='John Doe', email='johndoe@example.com')
user2 = User(name='Jane Doe', email='janedoe@example.com')
session.add(user1)
session.add(user2)

# Commit the transaction
session.commit()

# Close the session
session.close()
