## Step 1: Prepare the Environment
### - Ensure that all necessary libraries and drivers are installed (e.g., `pandas`, `SQLAlchemy`, and appropriate database drivers such as `pyodbc`).
### - Verify that the Python environment is correctly configured to handle database operations.

## ------------------------ DONE ------------------------ 

## Step 2: Import Necessary Libraries
### - Import `pandas` for data manipulation, `SQLAlchemy` for ORM functionality, and other required libraries.

import pandas
# Import the necessary libraries
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

## ------------------------ DONE ------------------------ 


## Step 3: Load CSV Files
### - Use pandas to read CSV files from the specified directory. Ensure you handle any potential encoding issues or missing data during this step.


customers_df = pandas.read_csv('dbs/bakery/customers.csv')
goods_df = pandas.read_csv('dbs/bakery/goods.csv')
items_df = pandas.read_csv('dbs/bakery/items.csv')
receipts_df = pandas.read_csv('dbs/bakery/receipts.csv')

## Step 3a: Visualize columnn names and data types
print(customers_df.dtypes)
print(goods_df.dtypes)
print(items_df.dtypes)
print(receipts_df.dtypes)

## ------------------------ DONE ------------------------ 



## Step 4: Clean and Prepare Data
### - Inspect the dataframes for any inconsistencies, missing values, or data type discrepancies. Perform necessary data cleaning and transformation to match the target database schema.

#### Step 4a. Confirm that the id or id variable types are unique in each dataframe using code like the following:

##### i. Convert the unique values in 'id' columns from both dataframes to sets (Had to manually check the dataframes to see which column was the unique identifier)
# items_df_ids = set(items_df['id'].unique()) ## This is not going to be unique
customers_df_ids = set(customers_df['Id'].unique())
goods_df_ids = set(goods_df['Id'].unique())
receipts_df_ids = set(receipts_df['RecieptNumber'].unique())

## check to see if the ids are unique
if len(customers_df_ids) == len(customers_df):
    print("The ids in the customers dataframe are unique.")

if len(goods_df_ids) == len(goods_df):
    print("The ids in the goods dataframe are unique.")

if len(receipts_df_ids) == len(receipts_df):
    print("The ids in the receipts dataframe are unique.")


## ------------------------ DONE ------------------------ 


## Step 5: Establish Database Connection
### - Set up environment variables for sensitive information like database credentials (username, password, server address).
### - Create a connection to the Azure database using SQLAlchemy. This step should include configuring the connection string and establishing the connection using an engine and session object.

load_dotenv()

# Define server and database information
server_name = os.getenv('SERVER_NAME', 'default_server')
database = os.getenv('DATABASE_NAME', 'default_database')
username = os.getenv('DB_USERNAME', 'default_username')
password = os.getenv('DB_PASSWORD', 'default_password')
driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')

# Create the database engine for SQL Server
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server_name}/{database}?driver={driver}')
## ------------------------ DONE ------------------------ 



## Step 6: Define Database Schema
### - Define or confirm the schema of the target database tables if not already existing. This involves setting up classes in SQLAlchemy to mirror the tables you intend to upload the data to, which could also include defining relationships between tables if necessary.




Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    Id = Column(Integer, primary_key=True)
    LastName = Column(String)
    FirstName = Column(String)

class Good(Base):
    __tablename__ = 'goods'
    Id = Column(Integer, primary_key=True)
    Flavor = Column(String)
    Food = Column(String)
    Price = Column(Numeric)

class Receipt(Base):
    __tablename__ = 'receipts'
    ReceiptNumber = Column(Integer, primary_key=True)
    Date = Column(Date)
    CustomerId = Column(Integer, ForeignKey('customers.Id'))
    customer = relationship("Customer", back_populates="receipts")

class Item(Base):
    __tablename__ = 'items'
    Receipt = Column(Integer, ForeignKey('receipts.ReceiptNumber'), primary_key=True)
    Ordinal = Column(Integer, primary_key=True)
    Item = Column(Integer, ForeignKey('goods.Id'))
    good = relationship("Good")

# Establishing relationships
Customer.receipts = relationship("Receipt", order_by=Receipt.ReceiptNumber, back_populates="customer")
Good.items = relationship("Item", order_by=Item.Ordinal)

# Assuming engine is already created as per the previous code snippet
# Create all tables in the database
Base.metadata.create_all(engine)