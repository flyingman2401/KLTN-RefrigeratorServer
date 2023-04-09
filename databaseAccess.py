# MongoDB functions

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
    
def getLatestCollectionItem(mycol):
    item_details = mycol.find_one(sort =[('_id', pymongo.DESCENDING)])
    return item_details

def listCollectionItem (mycol):
    list = []
    for item in mycol.find({}):
        list.append(json.loads(json_util.dumps(item)))
    return list

def findCollectionItem(mycol, filter):
    userdata = mycol.find_one(filter)
    return userdata

def emptyCollection(mycol):
    x = mycol.remove()
    return x

def removeCollectionItem(mycol, data):
    x = mycol.delete_one(data)
    return x

def findUser(mycol, email):
    userdata = mycol.find_one({'email': email})
    return userdata

def saveUserToken(mycol, email, token):
    x = mycol.update_one(
        {'email': email},
        {"$set": {'token': token}}
    )
    return x