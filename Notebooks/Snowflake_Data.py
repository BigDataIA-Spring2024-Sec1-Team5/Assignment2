import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Snowflake connection parameters
snowflake_username = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASS')
snowflake_account = os.getenv('SNOWFLAKE_ACC_ID')

# Snowflake connection details
snowflake_connection = {
    'user': snowflake_username,
    'password': snowflake_password,
    'account': snowflake_account,
}

# Creating a connection to Snowflake
conn = snowflake.connector.connect(**snowflake_connection)

# Creating a cursor
cur = conn.cursor()

# Creating a database and table
create_database_query = "CREATE OR REPLACE DATABASE CFA_Data;"
create_table_query = """CREATE OR REPLACE
 TABLE CFA (
    name_of_topic VARCHAR,
    year VARCHAR,
    level VARCHAR,
    introduction VARCHAR,
    learning_outcomes VARCHAR,
    summary VARCHAR,
    link_to_summary_page VARCHAR,
    link_to_pdf_file VARCHAR
);"""

# Loading data from CSV into a DataFrame
df = pd.read_csv('Team05.csv')

# Replacing null values with the string 'NULL'
df.fillna('None', inplace=True)

# Trying to create the database and table, then insert data into the table
try:
    # Executing create database query
    cur.execute(create_database_query)

    # Switching to the database
    cur.execute("USE DATABASE CFA_Data")

    # Creating the table
    cur.execute(create_table_query)

    # Inserting data into the table
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO CFA
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, row.tolist())

    print("Data successfully inserted into Snowflake.")
except Exception as e:
    print("An error occurred:", e)
finally:
    # Closing cursor
    cur.close()

    # Closing connection
    conn.close()
