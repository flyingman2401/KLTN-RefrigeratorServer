import json
from flask import jsonify
import databaseAccess

def addFood (mycol, data):
    return databaseAccess.insertCollectionItem(mycol, json.loads(data))
    
def removeFood (mycol, data):
    return databaseAccess.removeCollectionItem(mycol, json.loads(data))
        

    