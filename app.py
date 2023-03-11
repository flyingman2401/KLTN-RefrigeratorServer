from flask import Flask, request
from flask_jsonpify import jsonify
import databaseAccess

app = Flask(__name__)

# define mongoDB clients
connectionString = "mongodb+srv://19522437:trinhtrung12@kltn-refrigerator.qbihwdd.mongodb.net/test"

lastData = {
    "Nhiet do": "0",
    "Do am":"0"
}

@app.route('/')
def hello():
    return "Hello tủ lạnh siêu thông minh!"

@app.route('/SensorsData', methods = ['GET', 'POST'])
def handleRequests():
    if request.method == 'POST':
        data = request.get_json()
        lastData['Nhiet do'] = data['temp']
        lastData['Do am'] = data['humi']
        mycol = databaseAccess.accessCollection(connectionString, "sensors", "data")
        if databaseAccess.insertCollectionItem(mycol, data):
            return 'POST SUCCESS!'
        else:
            return 'POST FAILED!'
        
    elif request.method == 'GET':
        mycol = databaseAccess.accessCollection(connectionString, "sensors", "data")
        
        return lastData

if __name__ == '__main__':
   app.run(debug = True)
