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

sl_conn = sqlite3.connect('titanic.sqlite3')
sl_curs = sl_conn.cursor()

row_count = "SELECT COUNT(*) FROM titanic;"
sl_curs.execute(row_count).fetchall()

get_rows = "SELECT * FROM titanic;"
rows = sl_curs.execute(get_rows).fetchall()

get_prob_rows = "SELECT * FROM titanic where name like 'Miss. Ellen O%'"
prob_rows = sl_curs.execute(get_prob_rows).fetchall()

for row in rows:
    # print(row[3])
    # row[3] = row[3].replace("'", "''")
    # if ("'" in row[3]):
    #   continue
    print(row)
    print(type(row[3]))
    row = str(row[1:])

    # print(row)
    insert_row = """
    INSERT INTO titanic
    (survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare)
    VALUES """ + row + ";"
    # print(insert_row)
    cursor.execute(insert_row)
connection.commit()

cursor.execute("SELECT count(*) FROM titanic")
res = cursor.fetchall()
pprint(res)




