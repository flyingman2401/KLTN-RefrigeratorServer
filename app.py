from flask import Flask, request
from flask_jsonpify import jsonify
import databaseAccess
from bson import json_util, ObjectId
import json

app = Flask(__name__)

# define mongoDB clients
connectionString = "mongodb+srv://19522437:trinhtrung12@kltn-refrigerator.qbihwdd.mongodb.net/test"

@app.route('/')
def hello():
    return "Hello tủ lạnh siêu thông minh!"

@app.route('/SensorsData', methods = ['GET', 'POST'])
def handleRequests():

    if request.method == 'POST':
        data = request.get_json()
        mycol = databaseAccess.accessCollection(connectionString, "sensors", "data")
        if databaseAccess.insertCollectionItem(mycol, data):
            return 'POST SUCCESS!'
        else:
            return 'POST FAILED!'
        
    elif request.method == 'GET':
        mycol = databaseAccess.accessCollection(connectionString, "sensors", "data")
        data = databaseAccess.getLatestCollectionItem(mycol)
        return json.loads(json_util.dumps(data))
        return "GET DONE!"

if __name__ == '__main__':
   app.run(debug = True)
