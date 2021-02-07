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
collection = db.titanic_docs

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names())
# print(collection.count_documents({"name": ""}))

total_doc = collection.aggregate([{
    '$group': {
        '_id': 'null',
        'count': {'$sum': 1}
    }
}])
print("total document: ",list(total_doc))
print("anouther way of total document: ",collection.count_documents({}))

print("How many passengers survived, and how many died?")
pprint(len(list(collection.find({'Survived': 1}))))
# not working
# total_survived = collection.aggregate([{
#     '$group': {
#         '_id': 'Survived',
#         'count': {'$sum': 1}
#     }
# }])
# print("total_survived", list(total_survived))
print("and how many died?")
pprint(len(list(collection.find({'Survived': 0}))))

print("How many passengers were in each class?")
passengers_each_class = collection.aggregate([{
    '$group': { 
        '_id': "$Pclass", 
        'total': { '$sum': 1 } 
    } 
}])
pprint(list(passengers_each_class))

print("How many passengers survived within each class?")
survived_num_each_class = collection.aggregate([
    { '$match': { 'Survived': 1 } },
    {
        '$group': { 
            '_id': "$Pclass", 
            'survived': { '$sum': 1 }
        } 
    }
])
pprint(list(survived_num_each_class))

print("How many passengers died within each class?")
died_num_each_class = collection.aggregate([
    { '$match': { 'Survived': 0 } },
    {
        '$group': { 
            '_id': "$Pclass", 
            'died': { '$sum': 1 }
        } 
    }
])
pprint(list(died_num_each_class))

print("What was the average age of survivors vs nonsurvivors?")
survived_died_ave_age = collection.aggregate([
    {
        '$group': { 
            '_id': "$Survived", 
            'averageAge': { '$avg': '$Age' }
        } 
    }
])
pprint(list(survived_died_ave_age))

print("What was the average age of each passenger class?")
pclass_ave_age = collection.aggregate([
    {
        '$group': { 
            '_id': "$Pclass", 
            'averageAge': { '$avg': '$Age' }
        } 
    }
])
pprint(list(pclass_ave_age))

print("What was the average fare by passenger class?")
pclass_ave_fare = collection.aggregate([
    {
        '$group': { 
            '_id': "$Pclass", 
            'averageFare': { '$avg': '$Fare' }
        } 
    }
])
pprint(list(pclass_ave_fare))
print("What was the average fare by survival?")

survive_ave_fare = collection.aggregate([
    {
        '$group': { 
            '_id': "$Survived", 
            'averageFare': { '$avg': '$Fare' }
        } 
    }
])
pprint(list(survive_ave_fare))


print("How many siblings/spouses aboard on average, by passenger class? By survival?")
pclass_ave_siblings = collection.aggregate([
    {
        '$group': { 
            '_id': "$Pclass", 
            'averageSiblings': { '$avg': '$Siblings-Spoused-Aboard' }
        } 
    }
])
pprint(list(pclass_ave_siblings))
survive_ave_siblings = collection.aggregate([
    {
        '$group': { 
            '_id': "$Survived", 
            'averageSiblings': { '$avg': '$Siblings-Spoused-Aboard' }
        } 
    }
])
pprint(list(survive_ave_siblings))
print("How many parents/children aboard on average, by passenger class? By survival?")
pclass_ave_parents = collection.aggregate([
    {
        '$group': { 
            '_id': "$Pclass", 
            'averageParents': { '$avg': '$Parents-Children-Aboard' }
        } 
    }
])
pprint(list(pclass_ave_parents))
survive_ave_parents = collection.aggregate([
    {
        '$group': { 
            '_id': "$Survived", 
            'averageParents': { '$avg': '$Parents-Children-Aboard' }
        } 
    }
])
pprint(list(survive_ave_parents))

pprint(collection.find_one({}))
print("Do any passengers have the same name?")
distinct_name = collection.distinct('Name')
print(len(list(distinct_name))) # total_document is 887, so no same name
# (Bonus! Hard, may require pulling and processing with Python)
print("How many married couples were aboard the Titanic?")
print("Assume that two people (one Mr. and one Mrs.) with the same last name and with at least 1 sibling/spouse aboard are a married couple.")
# collection.drop()
