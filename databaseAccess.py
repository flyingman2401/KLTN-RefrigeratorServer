import json
import pymongo
from bson import json_util

def accessCollection(connectionString, dbName, collectionName):
    myclient = pymongo.MongoClient(connectionString)
    mydb = myclient[dbName]
    mycol = mydb[collectionName]
    return mycol

def insertCollectionItem(mycol, data):
    x = mycol.insert_one(data)
    return x

def removeCollectionItem(mycol, data):
    x = mycol.delete_one(data)
    return x

def updateCollectionItem(mycol, query, value):
    x = mycol.update_one(query, {"$set": value})
    return x

def findCollectionItem(mycol, filter):
    userdata = mycol.find_one(filter)
    return userdata

def countCollectionItems(mycol): # add count by deviceID for futher purposes
    count = mycol.count_documents({})
    return count

def listCollectionItem(mycol, filter):
    list = []
    for item in mycol.find(filter):
        list.append(json.loads(json_util.dumps(item)))
    return list

def emptyCollection(mycol, filter):
    x = mycol.delete_many(filter)
    return x

def getTopCollectionItem(mycol, n):
    items = mycol.find(sort =[('_id', pymongo.DESCENDING)]).limit(n)
    return items