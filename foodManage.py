import json
from flask import jsonify
import databaseAccess
from bson import json_util

def addFood (mycol, data):
    return databaseAccess.insertCollectionItem(mycol, json.loads(data))
    
def removeFood (mycol, data):
    return databaseAccess.removeCollectionItem(mycol, json.loads(data))
        
def getFoodList (mycol):
    foodList = []

    for item in mycol.find({}):
        foodList.append(json.loads(json_util.dumps(item)))

    if len(foodList) == 0:
        return None
    
    return foodList
    
    

    