import pymongo
import os
from dotenv import load_dotenv
import sqlite3
from pprint import pprint

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

connection_uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}-shard-00-00.nhxw7.mongodb.net:27017,{CLUSTER_NAME}-shard-00-01.nhxw7.mongodb.net:27017,{CLUSTER_NAME}-shard-00-02.nhxw7.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-mcpbmz-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_uri)
db = client.titanic_database
print("COLLECTIONS:")
print(db.list_collection_names())
collection = db.titanic_docs
print("DOCS:", collection.count_documents({}))
# print(collection.count_documents({"name": ""}))

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "module2-sql-for-analysis", "titanic.sqlite3")
sl_conn = sqlite3.connect(DB_FILEPATH)
sl_curs = sl_conn.cursor()

# get_rows = "SELECT * FROM titanic;"
# rows = sl_curs.execute(get_rows).fetchall()

# for row in rows:
#     pprint(row)
#     row_doc = {
#         'Survived': row[1],
#         'Pclass': row[2],
#         'Name': row[3],
#         'Sex': row[4],
#         'Age': row[5],
#         'Siblings-Spoused-Aboard': row[6],
#         'Parents-Children-Aboard': row[7],
#         'Fare': row[8]
#     }
#     collection.insert_one(row_doc)
print("~~~~~")
pprint(len(list(collection.find({'Survived': 1}))))