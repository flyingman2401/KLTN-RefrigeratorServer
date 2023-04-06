from  werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, request
from bson import json_util
import databaseAccess
import json
import handleToken
import foodManage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Refrigerator'

# define mongoDB cloud connection string
connectionString = "mongodb+srv://19522437:trinhtrung12@kltn-refrigerator.qbihwdd.mongodb.net/test"
sensorsDataCollection = databaseAccess.accessCollection(connectionString, "sensors", "data")
userInformationCollection = databaseAccess.accessCollection(connectionString, "accounts", "user")
FoodInsideFridgeCollection = databaseAccess.accessCollection(connectionString, "FoodManagement", "FoodInsideFridge")

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
    
@app.route('/login', methods = ['GET'])
def handleLoginRequests():
    data = request.headers.get('Authorization')
    print(request.headers)

    if (data.split()[0] == 'Basic'):
        email = request.authorization.username
        password = request.authorization.password
        # check if user is exist in database
        user = databaseAccess.findUser(userInformationCollection, email)
        if not user:
            return make_response('Khong ton tai nguoi dung!', 401)
        
        # check password and generate token key if correct    
        if check_password_hash(user['password'], password):
            token = handleToken.generateToken(email, app.config['SECRET_KEY'], userInformationCollection)
            return make_response(jsonify({'token' : token}), 201)
        else:
            return make_response('Khong the xac thuc nguoi dung!', 401)
        
    elif (data.split()[0] == 'Bearer'):
        token = data.split()[1]
        email =  handleToken.checkToken(token, app.config['SECRET_KEY'], userInformationCollection)

        if email == None:
            return make_response('Not Authorized!', 401)
        
        token = handleToken.generateToken(email, app.config['SECRET_KEY'], userInformationCollection)
        if token != None:
            response = make_response('OK', 200)
            response.headers['Authorization'] = token
            return response
        else:
            return make_response('Server failed to refresh token', 500)

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
            'password': generate_password_hash(password),
            'token': ""
        }
        # insert user data to database
        if databaseAccess.insertCollectionItem(userInformationCollection, user):
            return make_response('Dang ky nguoi dung thanh cong!', 201)
    else:
        return make_response('Da ton tai nguoi dung!', 202)

@app.route('/FoodManagement', methods = ['GET', 'POST'])
def handleFoodManagement():

    # action 0: add food into fridge
    # action 1: remove food from fridge
    # action 2: get food list depend on page
    data = request.get_json()

    if (request.method == 'GET'):
        if (data['action'] == 2):
            foodList = foodManage.getFoodList(FoodInsideFridgeCollection)

            data = {
                "count":len(foodList),
                "data":foodList
            }

            if foodList != None:
                return make_response(data, 200)
            else:
                return make_response('Không thể tải danh sách!', 500)
    
    elif (request.method == 'POST'):
        x = False
        if (data['action'] == 0):
            x = foodManage.addFood(FoodInsideFridgeCollection, data['data'])
        elif (data['action'] == 1):
            x = foodManage.removeFood(FoodInsideFridgeCollection, data['data'])

        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)
        
        

if __name__ == '__main__':
   app.run(debug = True)
