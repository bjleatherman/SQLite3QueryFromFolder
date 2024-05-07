import sqlite3
import warnings
import pandas as pd
import datetime
import os

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Path to the SQLite database folder
file_path = r'input folder'

# SQL query as a string variable
query = ''' Query Here '''

# Specify the path to the Excel file where the result will be saved
excel_path = r'ouput filepath'

# Check if the CSV file already exists
if os.path.exists(excel_path):
    # Load existing CSV into DataFrame
    existing_df = pd.read_csv(excel_path)
else:
    existing_df = pd.DataFrame()  # Create an empty DataFrame if the CSV file doesn't exist

# Loop counter
counter = 0

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
            # Execute the query and load the result into a pandas DataFrame
            df = pd.read_sql_query(query, conn)

            # Close the database connection
            conn.close()

            if df.empty:
                print(f"The file {filename} resulted in an empty DataFrame.")

            # Append new data to the existing DataFrame and ignore FutureWarning temporarily
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                existing_df = pd.concat([existing_df, df], ignore_index=True)

            # Write the combined DataFrame to CSV
            existing_df.to_csv(excel_path, index=False)

        except Exception as e:
            print(f'ERROR: {filename}. {e}')

print("Data has been written to", excel_path)

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
