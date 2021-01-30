import sqlite3
from pprint import pprint
import pandas as pd
from sqlalchemy import create_engine

# engine = create_engine('sqlite:///buddymove_holidayiq.sqlite3', echo=False)

# df = pd.read_csv('buddymove_holidayiq.csv')
# print(df)
# df.to_sql('review', con=engine)
conn = sqlite3.connect('buddymove_holidayiq.sqlite3')

# print(engine)
# print(engine.execute("SELECT COUNT(*) FROM review").fetchall())
# print(engine.execute("SELECT COUNT(*) FROM review").fetchall())
# print(engine.execute("SELECT COUNT(*) FROM review").fetchall())

curs = conn.cursor()
TOTAL_REVIEWS = 'SELECT COUNT(*) FROM review'
curs.execute(TOTAL_REVIEWS)
print(curs.execute(TOTAL_REVIEWS).fetchall())

OVERLAP = 'SELECT COUNT(*) FROM review WHERE Nature >= 100 AND Shopping >= 100'
curs.execute(OVERLAP)
print(curs.execute(OVERLAP).fetchall())
