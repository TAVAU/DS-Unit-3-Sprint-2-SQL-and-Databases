import sqlite3
from queries import queries
from pprint import pprint

conn = sqlite3.connect('rpg_db.sqlite3')
# print("CONNECTION:", type(conn)) #> <class 'sqlite3.Connection'>

# h/t: https://kite.com/python/examples/3884/sqlite3-use-a-row-factory-to-access-values-by-column-name
# conn.row_factory = sqlite3.Row

curs = conn.cursor()
# print("CURSOR:", type(curs)) #> <class 'sqlite3.Cursor'>


for query in queries:
    print("--------------")
    print(f"QUERY: '{query['name']}'")

    #obj = curs.execute(query)
    #print("OBJ", type(obj))
    #print(obj) #> <class 'sqlite3.Cursor'>

    results = curs.execute(query['value']).fetchall()
    # print("RESULTS:", type(results)) # list
    # pprint(results)

    # print("FIRST RESULTS:", type(results[0])) #> type(results[0])
    for result in results:
        pprint(result)
    # breakpoint()