
library(DBI)
library(odbc)

# Load environment variables, assuming a .Renviron file in the working directory
# Make sure to define SERVER_NAME, DATABASE_NAME, DB_USERNAME, DB_PASSWORD, DB_DRIVER in your .Renviron
server_name <- Sys.getenv('SERVER_NAME')
database <- Sys.getenv('DATABASE_NAME')
username <- Sys.getenv('DB_USERNAME', 'default_username')
password <- Sys.getenv('DB_PASSWORD', 'default_password')
driver <- Sys.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

# Create the database connection string
conn_str <- paste0("Driver=", driver, ";Server=", server_name, 
                   ";Database=", database, ";UID=", username, 
                   ";PWD=", password, ";")

# Connect to the database
conn <- dbConnect(odbc::odbc(), .connection_string = conn_str)

# Get and print the table names
table_names <- dbListTables(conn)
print(table_names)

# Disconnect
dbDisconnect(conn)