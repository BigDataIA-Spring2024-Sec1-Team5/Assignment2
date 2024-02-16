import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
from sqlalchemy.engine import URL
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

# Loading data from CSV into DataFrames
df1 = pd.read_csv('2024-l1-topics-combined_structured-metadata.csv')
df2 = pd.read_csv('2024-l2-topics-combined_structured-metadata.csv')
df3 = pd.read_csv('2024-l3-topics-combined_structured-metadata.csv')

# Adding 'link' column to DataFrames
df1['link'] = 'https://cfa-assignment2.s3.us-east-2.amazonaws.com/data/Grobid_RR_2024_LevelI_combined.txt'
df2['link'] = 'https://cfa-assignment2.s3.us-east-2.amazonaws.com/data/Grobid_RR_2024_LevelII_combined.txt'
df3['link'] = 'https://cfa-assignment2.s3.us-east-2.amazonaws.com/data/Grobid_RR_2024_LevelIII_combined.txt'

# Renaming columns
df1.rename(columns={'Heading': 'heading', 'Paragraph': 'paragraph'}, inplace=True)
df2.rename(columns={'Heading': 'heading', 'Paragraph': 'paragraph'}, inplace=True)
df3.rename(columns={'Heading': 'heading', 'Paragraph': 'paragraph'}, inplace=True)

# Trying to create the databases, tables, and insert data into the tables
try:
    # Executing create database queries
    #cur.execute("CREATE OR REPLACE DATABASE CFA_Data;")

    # Switching to the database
    cur.execute("USE DATABASE CFA_Data")

    # Creating tables and inserting data
    for i, df in enumerate([df1, df2, df3], start=1):
        table_name = f"Metadata{i}"
        create_table_query = f"""
            CREATE OR REPLACE TABLE {table_name} (
                heading VARCHAR,
                paragraph VARCHAR,
                link VARCHAR
            )
        """
        cur.execute(create_table_query)

        # Inserting data into the table
        for index, row in df.iterrows():
            cur.execute(f"""
                INSERT INTO {table_name} (heading, paragraph, link)
                VALUES (%s, %s, %s)
            """, (row['heading'], row['paragraph'], row['link']))

    print("Data successfully inserted into Snowflake.")
except Exception as e:
    print("An error occurred:", e)
finally:
    # Closing cursor
    cur.close()

    # Closing connection
    conn.close()
