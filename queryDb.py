import sqlite3
import warnings
import pandas as pd
import datetime
import os

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Path to the SQLite database folder
file_path = r'path to dbs'

# SQL query as a string variable
statements = 'statements here'

query = 'query here' 

split_statments = statements.split(';')

# Specify the path to the Excel file where the result will be saved
excel_path = r'path to output file'

# Check if the CSV file already exists
if os.path.exists(excel_path):
    # Load existing CSV into DataFrame
    existing_df = pd.read_csv(excel_path)
else:
    existing_df = pd.DataFrame()  # Create an empty DataFrame if the CSV file doesn't exist

# Loop counter
counter = 0
empty_df_counter = 0
error_counter = 0
empty_file_list = []
error_file_list = []

# Iterate through each .db file in the file_path
for filename in os.listdir(file_path):

    print(f'counter: {counter}')
    counter += 1

    if filename.endswith(".db"):
        db_path = os.path.join(file_path, filename)
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)

        # Catch Errors
        try:
            # Create cursor object
            cur = conn.cursor()

            # Excecute SQL statements individually
            for statement in split_statments:
                statement = statement.strip()
                if statement:
                    cur.execute(statement)

            # Execute the query and load the result into a pandas DataFrame
            df = pd.read_sql_query(query, conn)

            # Close the database connection
            conn.close()

            if df.empty:
                print(f"The file {filename} resulted in an empty DataFrame.")
                empty_df_counter += 1
                empty_file_list.append(filename)

            # Append new data to the existing DataFrame and ignore FutureWarning temporarily
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                existing_df = pd.concat([existing_df, df], ignore_index=True)

            # Write the combined DataFrame to CSV
            existing_df.to_csv(excel_path, index=False)

        except Exception as e:
            print(f'ERROR: {filename}. {e}')
            error_counter += 1
            error_file_list.append(filename)
            #print(f'ERROR: {filename}')

print("Data has been written to", excel_path)
print(f'There were {empty_df_counter} empty results')
print(f'There were {error_counter} errors')

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
