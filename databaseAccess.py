# MongoDB functions

import pymongo

def accessCollection(connectionString, dbName, collectionName):
    myclient = pymongo.MongoClient(connectionString)
    mydb = myclient[dbName]
    mycol = mydb[collectionName]
    return mycol

def insertCollectionItem(mycol, data):
    x = mycol.insert_one(data)
    if (x):
        return 1
    else:
        return 0
    
def getLatestCollectionItem(mycol):
    item_details = mycol.find_one(sort =[('_id', pymongo.DESCENDING)])
    return item_details

def findUser(mycol, email):
    userdata = mycol.find_one({'email': email})
    return userdata

def saveUserToken(mycol, email, token):
    x = mycol.update_one(
        {'email': email},
        {"$set": {'token': token}}
    )
    if (x):
        return 1
    else:
        return 0