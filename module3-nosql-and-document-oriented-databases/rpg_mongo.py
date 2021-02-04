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

print("----------------")
print("URI:", connection_uri)

client = pymongo.MongoClient(connection_uri)
print("----------------")
print("CLIENT:", type(client), client)

db = client.rpg_database
print("----------------")
print("DB:", type(db), db)

collection = db.rpg_docs
print("----------------")
print("COLLECTION:", type(collection), collection)

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names())

print("DOCS:", collection.count_documents({}))
# print(collection.count_documents({"name": ""}))

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "module1-introduction-to-sql", "rpg_db.sqlite3")
sl_conn = sqlite3.connect(DB_FILEPATH)
sl_curs = sl_conn.cursor()

get_characters = "SELECT * FROM charactercreator_character;"
characters = sl_curs.execute(get_characters).fetchall()

# insert charactercreator_character

print(type(characters))
print(type(characters[0]))
print(type(characters[0][1]))
for character in characters:
    print(character[1])
    rpg_doc = {
        'name': character[1],
        'level': character[2],
        'exp': character[3],
        'hp': character[4],
        'strength': character[5],
        'intelligence': character[6],
        'dexterity': character[7],
        'wisdom': character[8],
        'items': [],
        'weapons': []
    }
    collection.insert_one(rpg_doc)

print("DOCS:", collection.count_documents({}))

# add items for characters
get_character_items = """
SELECT 
  c.character_id
  ,c.name as character_name
  ,i.item_id, i.name as item_name
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
LEFT JOIN armory_item i ON i.item_id = inv.item_id
"""
character_items = sl_curs.execute(get_character_items).fetchall()
pprint(character_items)

for character_item in character_items:
    character_name = character_item[1]
    query = { 'name': character_name }
    newvalues = { "$push": { "items":  character_item[3]} }
    collection.update_one(query, newvalues)

# add weapons for characters
get_character_weapons = """
SELECT 
  c.character_id
  ,c.name as character_name
  , w.item_ptr_id, i.name as weapon_name
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
LEFT JOIN armory_weapon w ON w.item_ptr_id = inv.item_id
JOIN armory_ITEM i ON i.item_id = w.item_ptr_id
"""
character_weapons = sl_curs.execute(get_character_weapons).fetchall()
pprint(character_weapons)

for character_weapon in character_weapons:
    character_name = character_weapon[1]
    query = { 'name': character_name }
    # newvalues = { "$pop": { "weapons": 1} }
    newvalues = { "$push": { "weapons":  character_weapon[3]} }
    collection.update_one(query, newvalues)

pprint(collection.find_one({'name': 'At id recusandae expl'}))
# collection.drop()


