from flask import Flask, request
from flask_jsonpify import jsonify

app = Flask(__name__)

lastData = {
    "temp": "0",
    "humid":"0"
}

@app.route('/')
def hello():
    return "Hello tủ lạnh siêu thông minh!"

@app.route('/SensorsData', methods = ['GET', 'POST'])
def receiveData():
    if request.method == 'POST':
        data = request.get_json()
        lastData['temp'] = data['temp']
        # temp = data['temp']
        # humid = data['humid']
        return data
        # return 'POST SUCCESS!'
    elif request.method == 'GET':
        # return jsonify(temp, humid)
        return lastData

if __name__ == '__main__':
   app.run(debug = True)
