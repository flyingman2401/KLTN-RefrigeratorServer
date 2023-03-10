from flask import Flask, request
from flask_jsonpify import jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Refrigerature\'s Server say hello to USER nhá!'

@app.route('/SensorsData', methods = ['GET', 'POST'])
def receiveData():
    if request.method == 'POST':
        return 'POST SUCCESS!'
    elif request.method == 'GET':
        return 'GET SUCCESS!'

if __name__ == '__main__':
   app.run(debug = True)
