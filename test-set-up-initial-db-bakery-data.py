## Step 1: Prepare the Environment
### - Ensure that all necessary libraries and drivers are installed (e.g., `pandas`, `SQLAlchemy`, and appropriate database drivers such as `pyodbc`).
### - Verify that the Python environment is correctly configured to handle database operations.

## ------------------------ DONE ------------------------ 

## Step 2: Import Necessary Libraries
### - Import `pandas` for data manipulation, `SQLAlchemy` for ORM functionality, and other required libraries.

import pandas
# Import the necessary libraries
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv



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