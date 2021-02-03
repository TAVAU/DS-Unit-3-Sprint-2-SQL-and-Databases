#https://api.elephantsql.com/console/ab6f9852-0171-487f-bce5-af53f7396a98/browser?
#https://github.com/s2t2/lambda-ds-3-2/blob/master/app/elephant_multi.py
import psycopg2
import sqlite3

host = 'ziggy.db.elephantsql.com'
dbname = 'dlniqsap'
user = 'dlniqsap'
password = 'sZjXypU1k_h2kmJjPuOWnv7kzi1Mp8iI'

pg_conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
pg_curs = pg_conn.cursor()

sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_curs = sl_conn.cursor()

row_count = "SELECT COUNT(*) FROM charactercreator_character;"
sl_curs.execute(row_count).fetchall()

get_characters = "SELECT * FROM charactercreator_character;"
characters = sl_curs.execute(get_characters).fetchall()

sl_curs.execute('PRAGMA table_info(charactercreator_character);').fetchall()

create_character_table = """
CREATE TABLE charactercreator_character (
  character_id  SERIAL PRIMARY KEY,
  name  varchar(30),
  level INT,
  exp  INT,
  hp INT,
  strength INT,
  intelligence INT,
  dexterity INT,
  wisdom INT
);
"""

pg_curs.execute(create_character_table)
pg_conn.commit()

for character in characters:
    insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ";"
    pg_curs.execute(insert_character)
pg_conn.commit()

pg_curs.execute("SELECT * FROM charactercreator_character")
pg_characters = pg_curs.fetchall()

# for(character, pg_character) in zip(characters, pg_characters):
#     assert character == pg_character