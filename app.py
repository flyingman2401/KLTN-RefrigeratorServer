from  werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, request
from bson import json_util
import databaseAccess
import json
import handleToken
import foodManage
from flask_mqtt import Mqtt
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Refrigerator'

# define mongoDB cloud connection string
connectionString = "mongodb+srv://19522437:trinhtrung12@kltn-refrigerator.qbihwdd.mongodb.net/test"
collectionList = {
    "User":"",
    "Device":"",
    "SersorsData":"",
    "Rating":"",
    "Dish":"",
    "Ingredient":"",
    "DishType":"",
    "IngredientInsideFridge":"", 
    "RecommendationDishes":""
}
for item in collectionList:
    collectionList[item] = databaseAccess.accessCollection(connectionString, "RefrigeratorManagement", item)

# config Flespi Broker parameters
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'XYwy6gDl0Y76a9C5vl18YJtp0RxQzkYm8iJ3occc078Z6BUqKLmzkGM8l9OLiAVe'
app.config['MQTT_PASSWORD'] = ''
mqtt = Mqtt(app)

# MQTT events handle

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    devicesList = databaseAccess.listCollectionItem(collectionList['Device'])
    for device in devicesList:
        mqtt.subscribe(device['id'] + '/SensorsData')
    print("MQTT Broker Connected")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    deviceID = topic.split('/')[0]
    mqttData = message.payload.decode().split(" ")
    time = datetime.now()
    if topic.split('/')[1] == 'SensorsData':
        data = {
            "deviceID": deviceID,
            "time": time,
            "temp": float(mqttData[0]),
            "humi": float(mqttData[1]),
        }
        databaseAccess.insertCollectionItem(collectionList['SensorsData'], data)

# app routes

@app.route('/')
def hello():
    return "Hello tủ lạnh siêu thông minh!"

@app.route('/SensorsData', methods = ['GET'])
def handle_requests():
    if request.method == 'GET':
        data = []
        limitItems = 10
        itemsCount = databaseAccess.countCollectionItems(collectionList['SensorsData'])
        if(itemsCount < limitItems):
            data = databaseAccess.getTopCollectionItem(collectionList['SensorsData'], itemsCount)
        else:
            data = databaseAccess.getTopCollectionItem(collectionList['SensorsData'], limitItems)
        return json.loads(json_util.dumps(data))

@app.route('/FoodManagement', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def handle_food_management():
    
    # POST method is used to add an ingredient to IngredientInsideFridge Collection
    # GET method is used to get list of data:
    # - action 1: get list of ingredients inside fridge
    # - action 2: get list of recommendation dishes
    # DELETE method is used to delete an ingredient in IngredientInsideFridge Collection

    if (request.method == 'POST'):
        data = request.get_json()
        x = databaseAccess.insertCollectionItem(collectionList['IngredientInsideFridge'], data)
        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)


    elif (request.method == 'GET'):
        args = request.args
        if (args.get("action", type=int) == 1):
            ingredientsList = foodManage.getFoodList(collectionList['IngredientInsideFridge'])
            return make_response(ingredientsList, 200)
        elif (args.get("action", type=int) == 2):
            rcmList = foodManage.getRecommendationList(collectionList['RecommendationDishes'], collectionList['Dish'], collectionList['Ingredient'])
            return make_response(rcmList, 200)
        else:
            return make_response('Không biết làm gì luôn??', 404)


    elif (request.method == 'DELETE'):
        data = request.get_json()
        x = foodManage.removeFood(collectionList['IngredientInsideFridge'], data)
        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)


    elif (request.method == 'PUT'):
        make_response("No implementation yet!")

      

# @app.route('/login', methods = ['GET'])
# def handle_login_requests():
#     data = request.headers.get('Authorization')
#     print(request.headers)

#     if (data.split()[0] == 'Basic'):
#         email = request.authorization.username
#         password = request.authorization.password
#         # check if user is exist in database
#         user = databaseAccess.findUser(userInformation_Collection, email)
#         if not user:
#             return make_response('Khong ton tai nguoi dung!', 401)
        
#         # check password and generate token key if correct    
#         if check_password_hash(user['password'], password):
#             token = handleToken.generateToken(email, app.config['SECRET_KEY'], userInformation_Collection)
#             return make_response(jsonify({'token' : token}), 201)
#         else:
#             return make_response('Khong the xac thuc nguoi dung!', 401)
        
#     elif (data.split()[0] == 'Bearer'):
#         token = data.split()[1]
#         email =  handleToken.checkToken(token, app.config['SECRET_KEY'], userInformation_Collection)

#         if email == None:
#             return make_response('Not Authorized!', 401)
        
#         token = handleToken.generateToken(email, app.config['SECRET_KEY'], userInformation_Collection)
#         if token != None:
#             response = make_response('OK', 200)
#             response.headers['Authorization'] = token
#             return response
#         else:
#             return make_response('Server failed to refresh token', 500)

# @app.route('/signup', methods = ['POST'])
# def handle_signup_requests():
#     data = request.get_json()
  
#     # gets name, email and password
#     name, email, password = data['name'], data['email'], data['password']
  
#     # checking for existing user
#     user = databaseAccess.findUser(userInformation_Collection, email)
    
#     # create user if not existing
#     if not user:
#         # user data in json object
#         user = {
#             'name': name,
#             'email': email,
#             'password': generate_password_hash(password),
#             'token': ""
#         }
#         # insert user data to database
#         if databaseAccess.insertCollectionItem(userInformation_Collection, user):
#             return make_response('Dang ky nguoi dung thanh cong!', 201)
#     else:
#         return make_response('Da ton tai nguoi dung!', 202)
  

if __name__ == '__main__':
   app.run(debug = True)
