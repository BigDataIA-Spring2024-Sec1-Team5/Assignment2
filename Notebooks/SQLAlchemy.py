from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL
import pandas as pd
import numpy as np

load_dotenv()

TABLE_NAME = 'CFA_Data'
DATABASE_NAME = 'CFA'
WAREHOUSE_NAME = 'DATA_WH'


base_url = URL.create(
    "snowflake",
    username=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASS'),
    host=os.getenv('SNOWFLAKE_ACC_ID'),
)

# Creating database for storing cfa data
create_cfa_database_query = f"CREATE OR REPLACE DATABASE {DATABASE_NAME};"

# Creating table for CFA Data
create_scraped_data_table_query = f"""CREATE OR REPLACE TABLE {TABLE_NAME} (
    link_summary STRING,
    topic STRING,
    year STRING,
    level STRING,
    link_pdf STRING,
    introduction TEXT,
    learning_outcomes TEXT,
    summary TEXT,
    PRIMARY KEY (link_summary)
)
"""

# Creating warehouse for the cfa databases
create_cfa_warehouse_query = f"""CREATE OR REPLACE WAREHOUSE {WAREHOUSE_NAME} WITH
    WAREHOUSE_SIZE = 'X-Small'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE; 
"""
# Executing Queries
def execute_ddl_queries(connection):
    connection.execute(create_cfa_database_query)
    connection.execute(create_scraped_data_table_query)
    connection.execute(create_cfa_warehouse_query)

# Uploading the dataframe
def read_and_upload_df(connection):
    connection.execute(f'USE WAREHOUSE {WAREHOUSE_NAME};')
    connection.execute(f'USE DATABASE {DATABASE_NAME};')

    df = pd.read_csv('Team05.csv')
    values_list = []
    for id, row in df.iterrows():
        values_list.append("('{link_summary}', '{topic}', {year}, '{level}', '{link_pdf}', '{intro}', '{learning_outcomes}', '{summary}')".format(
            link_summary='None' if pd.isnull(row.Link_to_the_Summary_Page) else row.Link_to_the_Summary_Page, topic='None' if pd.isnull(row.Name_of_the_topic) else row.Name_of_the_topic, year='None' if pd.isnull(row.Year) else row.Year, level='None' if pd.isnull(row.Level) else row.Level, link_pdf='None' if pd.isnull(row.Link_to_the_PDF_File) else row.Link_to_the_PDF_File
, intro='None' if pd.isnull(row.Introduction) else row.Introduction, learning_outcomes='None' if pd.isnull(row.Learning_Outcomes) else row.Learning_Outcomes, summary='None' if pd.isnull(row.Summary) else row.Summary
        ))
        

        if(len(values_list)%50 == 0):
            values_str = ','.join(values_list)
            execute_insertion(values_str=values_str, id=id)
            values_list = []
    
    if(len(values_list) > 0):
        values_str = ','.join(values_list)
        execute_insertion(values_str=values_str, id=len(df))

# Inserting the dataframe into Snowflake Table
def execute_insertion(values_str, id):
    try:
        print("Started upload")
        connection.execute("BEGIN")
        connection.execute(f"""INSERT INTO {TABLE_NAME}
                            VALUES
                            {values_str};""")
        connection.execute("COMMIT")
        print(f"Upload successful till record count: {id+1}")
    except Exception as e:
        connection.execute("ROLLBACK")
        print("Exception inserting rows into db. Rolling back! "+str(e))

engine = create_engine(base_url)

try:
    connection = engine.connect()
    execute_ddl_queries(connection=connection)
    read_and_upload_df(connection=connection)
except Exception as e:
    print(e)
finally:
    connection.close()
    engine.dispose()