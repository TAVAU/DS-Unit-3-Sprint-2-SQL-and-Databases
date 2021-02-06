import sqlite3
conn = sqlite3.connect('demo_data.sqlite3')
curs = conn.cursor()

drop_demo = "DROP TABLE IF EXISTS demo;"
curs.execute(drop_demo)
conn.commit()
create_demo = """
    CREATE TABLE demo (
        s TEXT PRIMARY KEY,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL
    )
    """
curs.execute(create_demo)

insert_demo = """
INSERT INTO demo (s, x, y)
VALUES 
   ('g', 3, 9),
   ('v', 5, 7),
   ('f', 8, 7);
"""
curs.execute(insert_demo)
conn.commit()

row_count_query  = "SELECT count(*) FROM demo"
curs.execute(row_count_query)
res = curs.fetchall()
row_count = res[0][0]
print("row_count: ", row_count) #3

xy_at_least_5_query = """
    SELECT count(*) FROM demo
    WHERE x >=5 AND y>=5;
"""
curs.execute(xy_at_least_5_query)
res = curs.fetchall()
xy_at_least_5 = res[0][0]
print("xy_at_least_5_query: ", xy_at_least_5) #2

unique_y_query  = "SELECT count(DISTINCT y) FROM demo"
curs.execute(unique_y_query)
res = curs.fetchall()
unique_y = res[0][0]
print("unique_y: ", unique_y) #2