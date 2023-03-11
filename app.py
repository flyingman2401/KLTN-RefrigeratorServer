from flask import Flask, request
from flask_jsonpify import jsonify

app = Flask(__name__)

lastData = {
    "Nhiet do": "0",
    "Do am":"0"
}

@app.route('/')
def hello():
    return "Hello tủ lạnh siêu thông minh!"

@app.route('/SensorsData', methods = ['GET', 'POST'])
def receiveData():
    if request.method == 'POST':
        data = request.get_json()
        lastData['Nhiet do'] = data['temp']
        lastData['Do am'] = data['humi']
        # temp = data['temp']
        # humid = data['humid']
        return 'POST SUCCESS!'
    elif request.method == 'GET':
        # return jsonify(temp, humid)
        return lastData

if __name__ == '__main__':
   app.run(debug = True)
