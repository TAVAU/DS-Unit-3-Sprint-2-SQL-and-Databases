import os
from dotenv import load_dotenv
import psycopg2
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
from pprint import pprint


load_dotenv() #> loads contents of the .env file into the script's environment

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")


connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR:", cursor)

# create titanic.sqlite3
# engine = create_engine('sqlite:///titanic.sqlite3', echo=False)
# df = pd.read_csv('titanic.csv')
# df.to_sql('titanic', con=engine)

sl_conn = sqlite3.connect('titanic.sqlite3')
sl_curs = sl_conn.cursor()

df = pd.read_csv('titanic.csv')
#for any passengers with a single quote in their names, remove it
df['Name'] = df['Name'].str.replace("'", "")
df.to_sql('titanic', sl_conn, if_exists='replace')

row_count = "SELECT COUNT(*) FROM titanic;"
sl_curs.execute(row_count).fetchall()

get_info = "SELECT * FROM titanic;"
info = sl_curs.execute(get_info).fetchall()

result = sl_curs.execute('PRAGMA table_info(titanic);').fetchall()
pprint(result)

create_sex_enum = "CREATE TYPE SEX AS ENUM ('male', 'female');"

create_titanic_table = """
CREATE TABLE titanic (
  person_id  SERIAL NOT NULL PRIMARY KEY,
  survived INT,
  pclass INT,
  name varchar(255),
  sex  TEXT,
  age FLOAT,
  siblings_spouses_aboard INT,
  parents_children_aboard INT,
  fare FLOAT
);
"""
# cursor.execute(create_sex_enum)
cursor.execute(create_titanic_table)
connection.commit()
