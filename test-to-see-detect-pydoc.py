import pyodbc

# Get a list of all available drivers
drivers = [driver for driver in pyodbc.drivers()]

# Check if 'ODBC Driver 17 for SQL Server' is in the list
if 'ODBC Driver 17 for SQL Server' in drivers:
    print("ODBC Driver 17 for SQL Server is installed")
else:
    print("ODBC Driver 17 for SQL Server is not installed")