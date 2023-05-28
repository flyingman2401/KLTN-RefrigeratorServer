from threading import Thread, Lock
from  werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
from bson import json_util
import databaseAccess
import json
import foodRcm
import foodManage
from flask_mqtt import Mqtt
from datetime import datetime
import surveyAPI


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = 'Refrigerator'

# define mongoDB cloud connection string
connectionString = "mongodb+srv://19522437:trinhtrung12@kltn-refrigerator.qbihwdd.mongodb.net/test"

collectionList = {
    "User":"",
    "Device":"",
    "SensorsData":"",
    "Rating":"",
    "Dish":"",
    "Ingredient":"",
    "DishType":"",
    "IngredientInsideFridge":"", 
    "RecommendationDish":"",
    "RecommendationMeal":""
}
for item in collectionList:
    collectionList[item] = databaseAccess.accessCollection(connectionString, "RefrigeratorManagement", item)

surveyCollectionList = {
    "SurveySelectedIgd":"",
    "SurveyRcmDish":"",
    "SurveyRcmMeal":""
}
for item in surveyCollectionList:
    surveyCollectionList[item] = databaseAccess.accessCollection(connectionString, "SurveyData", item)

# config web socket parameters
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
# thread = None
# thread_lock = Lock()


# config Flespi Broker parameters
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'XYwy6gDl0Y76a9C5vl18YJtp0RxQzkYm8iJ3occc078Z6BUqKLmzkGM8l9OLiAVe'
app.config['MQTT_PASSWORD'] = ''
mqtt = Mqtt(app)

# Web Socket handle

# def background_thread():
#     print("Thread start")
#     while True:
#         data = []
#         limitItems = 10
#         itemsCount = databaseAccess.countCollectionItems(collectionList['SensorsData'])
#         if(itemsCount < limitItems):
#             data = databaseAccess.getTopCollectionItem(collectionList['SensorsData'], itemsCount)
#         else:
#             data = databaseAccess.getTopCollectionItem(collectionList['SensorsData'], limitItems)
#         emit('sensorsDataList', json.loads(json_util.dumps(data)))
#         print("emit done")
#         socketio.sleep(10)

# @socketio.on('connect')
# def handle_socketio_connect():
#     background_thread()
#     print("Connected") 

# @socketio.on('client event')
# def test_connect(data):
#     print("Received client event: ")
#     print(data)

# MQTT events handle

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    devicesList = databaseAccess.listCollectionItem(collectionList['Device'], {})
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
            "device_id": deviceID,
            "data_time": time,
            "data_temp": float(mqttData[0]),
            "data_humi": float(mqttData[1]),
        }
        databaseAccess.insertCollectionItem(collectionList['SensorsData'], data)

# app routes

@app.route('/')
def hello():
    return "Chào!"

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

    if (request.method == 'POST'):
        data = request.get_json()
        x = databaseAccess.insertCollectionItem(collectionList['IngredientInsideFridge'], data)
        if (x):
            foodRcm.updateRcmDish(
                collectionList['Dish'],
                collectionList['IngredientInsideFridge'],
                collectionList['RecommendationDish'],
                collectionList['Rating'],
                data['user_id']
            ),
            foodRcm.updateRcmMeal(
                collectionList['Dish'],
                collectionList['IngredientInsideFridge'],
                collectionList['RecommendationDish'],
                collectionList['RecommendationMeal'],
                collectionList['Rating'],
                data['user_id']
            )
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)

    elif (request.method == 'GET'):
        args = request.args

        # action 1: get list of ingredients inside fridge
        if (args.get("action", type=int) == 1):
            listIngredient = foodManage.getListIngredientInsideFridge(
                collectionList['IngredientInsideFridge'],
                collectionList['Ingredient']
            )
            return make_response(listIngredient, 200)
        
        # action 2: get list of recommendation dishes
        elif (args.get("action", type=int) == 2):
            listRcmDish = foodManage.getListRecommedationDish(
                collectionList['RecommendationDish'], 
                collectionList['Dish'], 
                collectionList['Ingredient'],
                collectionList['DishType']
            )
            return make_response(listRcmDish, 200)
        
        # action 3: get list of recommendation meal
        elif (args.get("action", type=int) == 3):
            listRcmMeal = foodManage.getListRecommedationMeal(
                collectionList['RecommendationMeal'], 
                collectionList['Dish'], 
                collectionList['Ingredient'],
                collectionList['DishType']
            )
            return make_response(listRcmMeal, 200)
        
        else:
            return make_response('Không biết làm gì luôn??', 404)

    elif (request.method == 'DELETE'):
        data = request.get_json()
        x = foodManage.removeIngredient(collectionList['IngredientInsideFridge'], data)
        if (x):
            foodRcm.updateRcmDish(
                collectionList['Dish'],
                collectionList['IngredientInsideFridge'],
                collectionList['RecommendationDish'],
                collectionList['Rating'],
                data['user_id']
            ),
            foodRcm.updateRcmMeal(
                collectionList['Dish'],
                collectionList['IngredientInsideFridge'],
                collectionList['RecommendationDish'],
                collectionList['RecommendationMeal'],
                collectionList['Rating'],
                data['user_id']
            )
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)

    elif (request.method == 'PUT'):
        data = request.get_json()
        x = foodManage.updateIngredient(collectionList['IngredientInsideFridge'], data)
        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)

@app.route('/Rating', methods = ['POST', 'PUT'])
def handle_rating():    
    if (request.method == 'GET'):
        data = request.get_json()
        x = foodManage.rateDish(
            collectionList['Rating'],
            data
        )
        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)
    
    elif (request.method == 'PUT'):
        data = request.get_json()
        x = foodManage.rateDish(
            collectionList['Rating'],
            data
        )
        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)

@app.route('/RecommendSurvey', methods = ['GET'])
@cross_origin(supports_credentials=True)
def handle_recommend_survey():
    if (request.method == 'GET'):
        args = request.args

        # action 1: get list of ingredients inside fridge
        if (args.get("action", type=int) == 1):
            listIngredient = surveyAPI.getIgdList(collectionList['Ingredient'])
            return make_response(listIngredient, 200)
        if (args.get("action", type=int) == 2):
            igdList = request.get_json()
            print(igdList)
            specificDishes = surveyAPI.getSpecificDish(igdList, collectionList["Dish"])
            surveyAPI.saveSelectedIgd(igdList, surveyCollectionList['SurveySelectedIgd'])
            return make_response(specificDishes, 200)
        if (args.get("action", type=int) == 3):
            selectedDish = request.get_json()
            foodRcm.updateRcmDish(
                collectionList['Dish'],
                surveyCollectionList['SurveySelectedIgd'],
                surveyCollectionList['SurveyRcmDish'],
                collectionList['Rating'],
                "ANYNOMOUS001"
            ),
            listRcmDish = surveyAPI.getListRecommedationDish(surveyCollectionList['SurveyRcmDish'], collectionList['Dish'], selectedDish)
            return make_response(listRcmDish, 200)
        
        

@app.route('/RecommendSurvey/GetDish', methods = ['GET'])
@cross_origin(supports_credentials=True)
def handle_recommend_survey_get_dish():
    if (request.method == 'GET'):
        igdList = request.get_json()
        print(igdList)
        specificDishes = surveyAPI.getSpecificDish(igdList, collectionList["Dish"])
        surveyAPI.saveSelectedIgd(igdList, surveyCollectionList['SurveySelectedIgd'])
        return make_response(specificDishes, 200)

if __name__ == '__main__':
   app.run(debug = True)
#    socketio.run(app)
