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
db = client.rpg_database
collection = db.rpg_docs

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names())
# print(collection.count_documents({"name": ""}))

print("How many total Characters are there?")
print(collection.count_documents({}))

print("How many Items does each character have? (Return first 20 rows)")
character_item = collection.aggregate([{'$project': { 'name': 1 ,'item_count': { '$size' :"$items" }}}])
pprint(list(character_item)[:20])
print("----------------")
print("How many Weapons does each character have? (Return first 20 rows)")
character_weapon = collection.aggregate([{'$project': { 'name': 1 ,'weapon_count': { '$size' :"$weapons" }}}])
pprint(list(character_weapon)[:20])
print("------------------")
# pprint(collection.find_one({}))
print("On average, how many Items does each Character have?")
character_item_stage = {'$project': { 'name': 1 ,'item_count': { '$size' :"$items" }}}
character_item_avg = collection.aggregate(
    [
        character_item_stage,
        {
            "$group": { 
                "_id": 0, 
                "character_item_avg": { "$avg": "$item_count" }
            }
        }
    ]
)
pprint(list(character_item_avg))
print("------------------")
print("On average, how many Weapons does each character have?")
character_weapon_stage = {'$project': { 'name': 1 ,'weapon_count': { '$size' :"$weapons" }}}
character_weapon_avg = collection.aggregate(
    [
        character_weapon_stage,
        {
            "$group": { 
                "_id": 0, 
                "character_weapon_avg": { "$avg": "$weapon_count" }
            }
        }
    ]
)
pprint(list(character_weapon_avg))
collection = db.rpg_armory
print("How many total Items?")
print(collection.count_documents({}))

print("How many of the Items are weapons? ")
print(len(list(collection.find({'weapon': {"$exists": True}}))))

print("How many are not?")
print(len(list(collection.find({'weapon': {"$exists": False}}))))
# pprint(collection.find_one({'name': 'At id recusandae expl'}))
# collection.drop()
