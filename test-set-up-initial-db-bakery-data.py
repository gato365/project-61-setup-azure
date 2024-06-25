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



# Step 1: Combine 'Receipt' and 'Ordinal' to create a unique identifier
mod_1_items_df = items_df.copy()
mod_1_items_df['unique_id'] =mod_1_items_df['Receipt'].astype(str) + '-' + mod_1_items_df['Ordinal'].astype(str)

# Step 2: Convert the combined column to a set to remove duplicates
unique_ids = set(mod_1_items_df['unique_id'])

# Step 3: Check if the length of the set is equal to the length of the DataFrame
if len(unique_ids) == len(mod_1_items_df):
    print("Each combination of Receipt and Ordinal in the items dataframe is unique.")
else:
    print("There are duplicate combinations of Receipt and Ordinal in the items dataframe.")
 
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
    Id = Column(String, primary_key=True)
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
    Item = Column(String, ForeignKey('goods.Id'))  # Updated data type to String
    good = relationship("Good")

# Establishing relationships
Customer.receipts = relationship("Receipt", order_by=Receipt.ReceiptNumber, back_populates="customer")
Good.items = relationship("Item", order_by=Item.Ordinal)

# Assuming engine is already created as per the previous code snippet
# Create all tables in the database
### (IMPORTANT: to run)
# Base.metadata.create_all(engine)


## ------------------------ DONE ------------------------ 

## Step 7: Validate Data against Schema
### - Ensure that the dataframe conforms to the database schema constraints such as data types, required fields, and unique constraints to avoid runtime errors during the upload process.


## Step 7a: Customers DataFrame Validation
### Step 7a i: Data Types Validation
#### Define the expected data types for the customers dataframe
expected_dtypes_customers = {
    'Id': 'int64',  
    'LastName': 'object',
    'FirstName': 'object'
}

issues_found = False
for column, expected_dtype in expected_dtypes_customers.items():
    if customers_df[column].dtype != expected_dtype:
        print(f"Customers - Column {column} has incorrect type {customers_df[column].dtype}, expected {expected_dtype}")
        issues_found = True
if not issues_found:
    print("Customers - All columns have the correct data type.")




#### Define the expected data types for the goods dataframe
expected_dtypes_goods = {
    'Id': 'object',  
    'Flavor': 'object',
    'Food': 'object',
    'Price': 'float64'
}

issues_found = False
for column, expected_dtype in expected_dtypes_goods.items():
    if goods_df[column].dtype != expected_dtype:
        print(f"Goods - Column {column} has incorrect type {goods_df[column].dtype}, expected {expected_dtype}")
        issues_found = True

if not issues_found:
    print("Goods - All columns have the correct data type.")

#### Define the expected data types for the items dataframe
expected_dtypes_items = {
    'Receipt': 'int64',  
    'Ordinal': 'int64',
    'Item': 'object'
}


issues_found = False
for column, expected_dtype in expected_dtypes_items.items():
    if items_df[column].dtype != expected_dtype:
        print(f"Items - Column {column} has incorrect type {items_df[column].dtype}, expected {expected_dtype}")
        issues_found = True

if not issues_found:
    print("Items - All columns have the correct data type.")


#### Define the expected data types for the receipts dataframe
expected_dtypes_receipts = {
    'RecieptNumber': 'int64',  
    'Date': 'object',
    'CustomerId': 'int64'
}

issues_found = False
for column, expected_dtype in expected_dtypes_receipts.items():
    if receipts_df[column].dtype != expected_dtype:
        print(f"Receipts - Column {column} has incorrect type {receipts_df[column].dtype}, expected {expected_dtype}")
        issues_found = True

if not issues_found:
    print("Receipts - All columns have the correct data type.")