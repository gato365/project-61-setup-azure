

## Step 1: Prepare the Environment
### - Ensure that all necessary libraries and drivers are installed (e.g., `pandas`, `SQLAlchemy`, and appropriate database drivers such as `pyodbc`).
### - Verify that the Python environment is correctly configured to handle database operations.

## DONE

## Step 2: Import Necessary Libraries
### - Import `pandas` for data manipulation, `SQLAlchemy` for ORM functionality, and other required libraries.

import pandas
import sqlalchemy
import pyodbc

## Step 3: Load CSV Files
### - Use pandas to read CSV files from the specified directory. Ensure you handle any potential encoding issues or missing data during this step.


list_df = pandas.read_csv('sample_database_example_students/list.csv')
teacher_df = pandas.read_csv('sample_database_example_students/teachers.csv')




## Step 4: Clean and Prepare Data
### - Inspect the dataframes for any inconsistencies, missing values, or data type discrepancies. Perform necessary data cleaning and transformation to match the target database schema.


#### Step 4a. Confirm that the Classroom variable is the same in both dataframes using code like the following:

##### i. Convert the unique values in 'Classroom' columns from both dataframes to sets
list_df_classrooms = set(list_df['Classroom'].unique())
teacher_df_classrooms = set(teacher_df['Classroom'].unique())

 
##### ii. Check if the sets are equal
if list_df_classrooms == teacher_df_classrooms:
    print("The Classroom variable numbers are the same in both dataframes.")
else:
    print("The Classroom variable numbers are not the same in both dataframes.")


## Step 5: Establish Database Connection
### - Set up environment variables for sensitive information like database credentials (username, password, server address).
### - Create a connection to the Azure database using SQLAlchemy. This step should include configuring the connection string and establishing the connection using an engine and session object.






## Step 6: Define Database Schema
### - Define or confirm the schema of the target database tables if not already existing. This involves setting up classes in SQLAlchemy to mirror the tables you intend to upload the data to, which could also include defining relationships between tables if necessary.

## Step 7: Validate Data against Schema
### - Ensure that the dataframe conforms to the database schema constraints such as data types, required fields, and unique constraints to avoid runtime errors during the upload process.

## Step 8: Upload Data to Database
### - Use the SQLAlchemy session to add data from the dataframe to the database. This could involve converting the dataframe into the defined SQLAlchemy ORM classes before adding and committing them to the database.

## Step 9: Handle Exceptions and Monitor Upload Process
### - Implement error handling to catch and log any issues that arise during the upload process. This helps in diagnosing and resolving issues without losing data integrity.

## Step 10: Verify and Validate Data Upload
### - Execute verification queries or use inspection tools to confirm that the data has been uploaded correctly and completely.

## Step 11: Close Database Connection
### - Properly close the database connection to free up resources. This should be done in a safe manner to ensure all transactions are completed before closure.

## Step 12: Clean-up and Final Checks
### - Perform any final clean-up actions, such as logging the upload history or sending notifications on the completion of the upload process.

