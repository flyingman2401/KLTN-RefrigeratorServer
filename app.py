from datetime import datetime, timedelta
from  werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, request
from bson import json_util
import databaseAccess
import json
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Refrigerator'

# define mongoDB cloud connection string
connectionString = "mongodb+srv://19522437:trinhtrung12@kltn-refrigerator.qbihwdd.mongodb.net/test"
sensorsDataCollection = databaseAccess.accessCollection(connectionString, "sensors", "data")
userInformationCollection = databaseAccess.accessCollection(connectionString, "accounts", "user")

@app.route('/')
def hello():
    return "Hello tủ lạnh siêu thông minh!"

@app.route('/SensorsData', methods = ['GET', 'POST'])
def handleRequests():

    if request.method == 'POST':
        data = request.get_json()
        if databaseAccess.insertCollectionItem(sensorsDataCollection, data):
            return 'POST SUCCESS!'
        else:
            return 'POST FAILED!'
        
    elif request.method == 'GET':
        data = databaseAccess.getLatestCollectionItem(sensorsDataCollection)
        return json.loads(json_util.dumps(data))
    
@app.route('/login', methods = ['POST'])
def handleLoginRequests():
    auth = request.get_json()
    
    # check if user is exist in database
    user = databaseAccess.findUser(userInformationCollection, auth['email'])
    if not user:
        return make_response('Khong ton tai nguoi dung!', 401)
    
    # check password and generate token key if correct    
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode({
            'public_id': user['email'],
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
        return make_response(jsonify({'token' : token}), 201)
    else:
        return make_response('Khong the xac thuc nguoi dung!', 401)

@app.route('/signup', methods = ['POST'])
def handleSignUpRequests():
    data = request.get_json()
  
    # gets name, email and password
    name, email, password = data['name'], data['email'], data['password']
  
    # checking for existing user
    user = databaseAccess.findUser(userInformationCollection, email)
    
    # create user if not existing
    if not user:
        # user data in json object
        user = {
            'name': name,
            'email': email,
            'password': generate_password_hash(password)
        }
        # insert user data to database
        if databaseAccess.insertCollectionItem(userInformationCollection, user):
            return make_response('Dang ky nguoi dung thanh cong!', 201)
    else:
        return make_response('Da ton tai nguoi dung!', 202)


if __name__ == '__main__':
   app.run(debug = True)
