from threading import Thread, Lock
from  werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin
from bson import json_util
import databaseAccess
import json
import foodRcm
import foodManage
from flask_mqtt import Mqtt
from datetime import datetime
import pytz
import surveyAPI

timezone = pytz.timezone('Asia/Ho_Chi_Minh')
app = Flask(__name__, static_folder='templates/static')
CORS(
    app, 
    origins=['*'], 
    methods=['GET', 'POST', 'OPTIONS'], 
    allow_headers=['application/json; charset=utf-8'],
    supports_credentials=True,
    resources={r"/*": {"origins": "*"}}
)
# app.config['CORS_HEADERS'] = 'Content-Type'
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
    "RecommendationMeal":"",
    "Disease": "",
    "History": "",
}
for item in collectionList:
    collectionList[item] = databaseAccess.accessCollection(connectionString, "RefrigeratorManagement", item)

surveyCollectionList = {
    "SurveySelectedIgd":"",
    "SurveyRcmDish":"",
    "SurveyRcmMeal":"",
    "SurveyHistory":"",
    "SurveyUserInfo":"",
}
for item in surveyCollectionList:
    surveyCollectionList[item] = databaseAccess.accessCollection(connectionString, "SurveyData", item)

# config Flespi Broker parameters
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'XYwy6gDl0Y76a9C5vl18YJtp0RxQzkYm8iJ3occc078Z6BUqKLmzkGM8l9OLiAVe'
app.config['MQTT_PASSWORD'] = ''
mqtt = Mqtt(app)

# MQTT events handle

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    devicesList = databaseAccess.listCollectionItem(collectionList['Device'], {})
    for device in devicesList:
        mqtt.subscribe(device['id'] + '/SensorsData')
    time = datetime.now(timezone)
    print(time)
    print("MQTT Broker Connected ")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    deviceID = topic.split('/')[0]
    print("\"" + message.payload.decode() + "\"")
    mqttMessage = message.payload.decode()
    if message.payload.decode().startswith(' '):
        mqttMessage = mqttMessage[1:]
    mqttData = mqttMessage.split(" ")
    time = datetime.now(timezone)
    if topic.split('/')[1] == 'SensorsData':
        data = {
            "device_id": deviceID,
            "data_time": time,
            "data_temp": float(mqttData[0]),
            "data_humi": float(mqttData[1]),
        }
        databaseAccess.insertCollectionItem(collectionList['SensorsData'], data)
    print("Received MQTT data at " + str(time) + ".")     

# app routes

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/UserData', methods = ['GET', 'POST', 'PUT'])
def handle_user():
    if request.method == 'GET':
        data = request.get_json()
        filter = {
            "id": data['user_id']
        }
        userData = databaseAccess.findCollectionItem(collectionList['User'], filter)
        print(userData)
        if (userData):
            return make_response(json_util.dumps(userData), 200)
        else:
            return make_response("Không tồn tại người dùng", 404)
    if request.method == 'PUT':
        data = request.get_json()
        filter = {
            "id": data['user_id']
        }
        userData = databaseAccess.findCollectionItem(collectionList['User'], filter)
        if (userData == None):
            return make_response("Không tồn tại người dùng", 404)
        databaseAccess.updateCollectionItem(collectionList['User'], filter, data)
        return make_response("Cập nhật thành công dữ liệu người dùng!", 200)
    
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
            time = datetime.now(timezone)
            foodRcm.collectionList = collectionList
            foodRcm.RecommendDishes(time, data['user_id'])
            foodRcm.RecommendMeals(time, data['user_id'])
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)

    elif (request.method == 'GET'):
        args = request.args

        # action 1: get list of ingredients inside fridge
        if (args.get("action", type=int) == 1):
            listIngredient = databaseAccess.listCollectionItem(collectionList['IngredientInsideFridge'], {})
            return make_response(listIngredient, 200)
        
        # action 2: get list of recommendation dishes
        elif (args.get("action", type=int) == 2):
            listRcmDish = databaseAccess.listCollectionItem(collectionList['RecommendationDish'], {}, "weight", -1)
            return make_response(listRcmDish, 200)
        
        # action 3: get list of recommendation meal
        elif (args.get("action", type=int) == 3):
            listRcmMeal = databaseAccess.listCollectionItem(collectionList['RecommendationMeal'], {}, "weight", -1)
            return make_response(listRcmMeal, 200)
        
        else:
            return make_response('Không biết làm gì luôn??', 404)

    elif (request.method == 'DELETE'):
        data = request.get_json()
        x = foodManage.removeIngredient(collectionList['IngredientInsideFridge'], data)
        if (x):
            time = datetime.now(timezone)
            foodRcm.collectionList = collectionList
            foodRcm.RecommendDishes(time, data['user_id'])
            foodRcm.RecommendMeals(time, data['user_id'])
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

@app.route('/FoodData', methods = ['GET'])
def handle_get_food_data():
    if (request.method == 'GET'):
        args = request.args

        # action 1: get list of ingredients
        if (args.get("action", type=int) == 1):
            listIngredient = databaseAccess.listCollectionItem(collectionList['Ingredient'], {})
            return make_response(listIngredient, 200)
        # action 2: get list of dishes
        elif (args.get("action", type=int) == 2):
            listDish = databaseAccess.listCollectionItem(collectionList['Dish'], {})
            return make_response(listDish, 200)
        # action 1: get list of dish types
        elif (args.get("action", type=int) == 3):
            listDishType = databaseAccess.listCollectionItem(collectionList['DishType'], {})
            return make_response(listDishType, 200)

@app.route('/Rating', methods = ['POST', 'PUT'])
def handle_rating():    
    if (request.method == 'POST'):
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

@app.route('/History', methods = ['GET', 'POST'])
def handle_history():
    if (request.method == 'POST'):
        data = request.get_json()
        x = foodManage.saveDishHistory(collectionList['History'], data)

        if (x):
            return make_response('Thanh cong!', 200)
        else:
            return make_response('Khong the thuc hien!', 500)
    elif (request.method == 'GET'):
        historyList = databaseAccess.listCollectionItem(collectionList['History'], {'user_id': "USER001"})
        return make_response(historyList, 200)

@app.route('/Recommendation', methods = ['GET'])
def handle_recommend():
    if (request.method == 'GET'):
        args = request.args
        # data = request.get_json()
        # action 1: get list of dishes
        if (args.get("action", type=int) == 1):
            time = datetime.now(timezone)
            print(time)
            foodRcm.collectionList = collectionList
            foodRcm.RecommendDishes(time, "USER001")
            listRcmDish = databaseAccess.listCollectionItem(collectionList['RecommendationDish'], {}, "weight", -1)
            return make_response(listRcmDish, 200)
        # action 2: get list of meals
        elif (args.get("action", type=int) == 2):
            time = datetime.now(timezone)
            print(time)
            foodRcm.collectionList = collectionList
            foodRcm.RecommendMeals(time, "USER001")
            listRcmMeal = databaseAccess.listCollectionItem(collectionList['RecommendationMeal'], {}, "weight", -1)
            return make_response(listRcmMeal, 200)


@app.route('/RecommendSurvey', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def handle_recommend_survey():
    if (request.method == 'GET'):
        args = request.args
        
        # action 1: get list of ingredients inside fridge
        if (args.get("action", type=int) == 1):
            listIngredient = surveyAPI.getIgdList(collectionList['Ingredient'])
            return make_response(listIngredient, 200)
        
    elif (request.method == 'POST'):
        args = request.args

        if (args.get("action", type=int) == 1):
            data = request.get_json()
            x = databaseAccess.insertCollectionItem(surveyCollectionList['SurveyUserInfo'], data)
            if x:
                return make_response("OK", 200)

        if (args.get("action", type=int) == 2):
            data = request.get_json()
            time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
            userID = data['user_id']
            igdList = data['ingredients']

            newCollectionList = collectionList
            newCollectionList['IngredientInsideFridge'] = surveyCollectionList['SurveySelectedIgd']
            newCollectionList['RecommendationDish'] = surveyCollectionList['SurveyRcmDish']
            newCollectionList['RecommendationMeal'] = surveyCollectionList['SurveyRcmMeal']
            newCollectionList['History'] = surveyCollectionList['SurveyHistory']
            newCollectionList['User'] = surveyCollectionList['SurveyUserInfo']

            databaseAccess.removeManyCollectionItem(newCollectionList['IngredientInsideFridge'], {"user_id": data['user_id']})
            
            foodRcm.collectionList = newCollectionList
            for igd in igdList:
                databaseAccess.insertCollectionItem(newCollectionList['IngredientInsideFridge'], igd)
            foodRcm.RecommendDishes(time, userID)
            listRcmDish = databaseAccess.listCollectionItem(newCollectionList['RecommendationDish'], {"user_id": data['user_id']}, "weight", -1)
            return make_response(listRcmDish, 200)
        
        if (args.get("action", type=int) == 3):
            data = request.get_json()
            time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
            userID = data['user_id']
            igdList = data['ingredients']

            newCollectionList = collectionList
            newCollectionList['IngredientInsideFridge'] = surveyCollectionList['SurveySelectedIgd']
            newCollectionList['RecommendationDish'] = surveyCollectionList['SurveyRcmDish']
            newCollectionList['RecommendationMeal'] = surveyCollectionList['SurveyRcmMeal']
            newCollectionList['History'] = surveyCollectionList['SurveyHistory']
            newCollectionList['User'] = surveyCollectionList['SurveyUserInfo']

            databaseAccess.removeManyCollectionItem(newCollectionList['IngredientInsideFridge'], {"user_id": data['user_id']})
            
            foodRcm.collectionList = newCollectionList
            for igd in igdList:
                databaseAccess.insertCollectionItem(newCollectionList['IngredientInsideFridge'], igd)
            foodRcm.RecommendDishes(time, userID)
            foodRcm.RecommendMeals(time, userID)
            listRcmMeal = databaseAccess.listCollectionItem(newCollectionList['RecommendationMeal'], {"user_id": data['user_id']}, "weight", -1)
            return make_response(listRcmMeal, 200)



FLUTTER_WEB_APP = 'templates/survey_app'

@app.route('/SurveyApp')
def render_page():
    return render_template('survey_app/index.html')


@app.route('/web/')
def render_page_web():
    return render_template('survey_app/index.html')


@app.route('/web/<path:name>')
def return_flutter_doc(name):
    datalist = str(name).split('/')
    DIR_NAME = FLUTTER_WEB_APP

    if len(datalist) > 1:
        for i in range(0, len(datalist) - 1):
            DIR_NAME += '/' + datalist[i]

    return send_from_directory(DIR_NAME, datalist[-1])
        
        
if __name__ == '__main__':
   app.run(debug = True)
