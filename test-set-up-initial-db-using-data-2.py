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

## ------------------------ DONE ------------------------ 






## Step 3: Load CSV Files
### - Use pandas to read CSV files from the specified directory. Ensure you handle any potential encoding issues or missing data during this step.


students_df = pandas.read_csv('sample_database_example_students/students.csv')
teachers_df = pandas.read_csv('sample_database_example_students/teachers.csv')

## ------------------------ DONE ------------------------ 




## Step 4: Clean and Prepare Data
### - Inspect the dataframes for any inconsistencies, missing values, or data type discrepancies. Perform necessary data cleaning and transformation to match the target database schema.


#### Step 4a. Confirm that the Classroom variable is the same in both dataframes using code like the following:

##### i. Convert the unique values in 'Classroom_ID' columns from both dataframes to sets
students_df_classrooms = set(students_df['Classroom_ID'].unique())
teachers_df_classrooms = set(teachers_df['Classroom_ID'].unique())

 
##### ii. Check if the sets are equal
if students_df_classrooms == teachers_df_classrooms:
    print("The Classroom variable numbers are the same in both dataframes.")
else:
    print("The Classroom variable numbers are not the same in both dataframes.")


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

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    grade = Column(Integer)
    classroom_id = Column(Integer, ForeignKey('teachers.classroom_id'))

class Teacher(Base):
    __tablename__ = 'teachers'
    classroom_id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    # The backref 'teacher' creates a virtual column in the Student model, linking each student to their teacher
    students = relationship("Student", backref="teacher")


## ------------------------ DONE ------------------------ 




## Step 7: Validate Data against Schema
### - Ensure that the dataframe conforms to the database schema constraints such as data types, required fields, and unique constraints to avoid runtime errors during the upload process.

#### Step 7a. Students DataFrame Validation
##### Step 7a i. Data Types Validation
expected_dtypes = {
    'ID': 'int64',  
    'LastName': 'object',
    'FirstName': 'object',
    'Grade': 'int64',
    'Classroom_ID': 'int64'
}

issues_found = False
for column, expected_dtype in expected_dtypes.items():
    if students_df[column].dtype != expected_dtype:
        print(f"Students - Column {column} has incorrect type {students_df[column].dtype}, expected {expected_dtype}")
        issues_found = True

if not issues_found:
    print("Students - All columns have the correct data type.")


##### Step 7a ii. Check for missing columns

required_columns = ['ID', 'LastName', 'FirstName', 'Grade', 'Classroom_ID']
missing_columns = [col for col in required_columns if col not in students_df.columns]
if missing_columns:
    print(f"Students - Missing required columns: {missing_columns}")
else:
    print("Students - All required columns are present.")





##### Step 7a ii. Check for null values in required columns
issues_found = False
null_checks = students_df[required_columns].isnull().sum()
for column, null_count in null_checks.items():
    if null_count > 0:
        print(f"Students - Column {column} contains {null_count} null values")
        issues_found = True

if not issues_found:
    print("Students - No null values found in required columns.")







#### Step 7b. Teachers DataFrame Validation
##### Step 7b i. Data Types Validation
expected_dtypes = {
    'Classroom_ID': 'int64',
    'LastName': 'object',
    'FirstName': 'object'
}

issues_found = False
for column, expected_dtype in expected_dtypes.items():
    if teachers_df[column].dtype != expected_dtype:
        print(f"Teachers - Column {column} has incorrect type {teachers_df[column].dtype}, expected {expected_dtype}")
        issues_found = True

if not issues_found:
    print("Teachers - All columns have the correct data type.")


##### Step 7b ii. Check for missing columns

required_columns = ['Classroom_ID', 'LastName', 'FirstName']
missing_columns = [col for col in required_columns if col not in teachers_df.columns]
if missing_columns:
    print(f"Teachers - Missing required columns: {missing_columns}")
else:
    print("Teachers - All required columns are present.")





##### Step 7b iii. Check for null values in required columns
issues_found = False
null_checks = teachers_df[required_columns].isnull().sum()
for column, null_count in null_checks.items():
    if null_count > 0:
        print(f"Teachers - Column {column} contains {null_count} null values")
        issues_found = True

if not issues_found:
    print("Teachers - No null values found in required columns.")


## ------------------------ DONE ------------------------ 














## Step 8: Upload Data to Database
### - Use the SQLAlchemy session to add data from the dataframe to the database. This could involve converting the dataframe into the defined SQLAlchemy ORM classes before adding and committing them to the database.

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
# Step 1: Convert DataFrame Rows to ORM Objects and Add to Session
# Adding students
for index, row in students_df.iterrows():
    student = Student(
        id=row['ID'],  # Assuming 'ID' is the column name in your DataFrame
        last_name=row['LastName'],
        first_name=row['FirstName'],
        grade=row['Grade'],
        classroom_id=row['Classroom_ID']
    )
    session.add(student)  # Step 2: Add ORM Object to Session

# Adding teachers
for index, row in teachers_df.iterrows():
    teacher = Teacher(
        classroom_id=row['Classroom_ID'],
        last_name=row['LastName'],
        first_name=row['FirstName']
    )
    session.add(teacher)

# Step 3: Commit the Session
try:
    session.commit()
    print("Data successfully added to the database.")
except Exception as e:
    session.rollback()  # Rollback the changes on error
    print(f"An error occurred: {e}")

# Step 4: Close the Session
session.close()

## ------------------------ DONE ------------------------
