from datetime import datetime
import databaseAccess

def getSpecificDish(igdList, dishCol):
    dishList = databaseAccess.listCollectionItem(dishCol, {})

    specificDishes = []
    for selectedigd in igdList:
        for dish in dishList:
            for igd in dish["dish_ingredients"]:
                if (igd[0] == selectedigd["id"]):
                    data = {
                        "id": dish["id"],
                        "dish_name": dish["dish_name"],
                        "dish_image": dish["dish_image"]
                    }
                    specificDishes.append(data)
                    break

    print(specificDishes)
    return specificDishes

def getIgdList(igdCol):
    igdList = []
    tempList = databaseAccess.listCollectionItem(igdCol, {})
    for igd in tempList:
        data = {
            "id": igd["id"],
            "ingredient_name": igd["ingredient_name"],
            "ingredient_image": igd["ingredient_image"],
            "ingredient_amount": 100,
            "ingredient_unit": igd["ingredient_unit"]
        }
        igdList.append(data)
    return igdList

def saveSelectedIgd(igdList, surveyIgdCol):
    databaseAccess.emptyCollection(surveyIgdCol, {})
    for igd in igdList:
        data = {
            "ingredient_id": igd["id"],
            "user_id": "ANYNOMOUS001",
            "food_manufacture": "Vasifood",
            "food_PRD": datetime.now().strftime('%Y-%m-%d'),
            "food_EXP": datetime.now().strftime('%Y-%m-%d'),
            "food_amount": igd["ingredient_amount"],
            "food_unit": igd["ingredient_unit"]
        }
        x = databaseAccess.insertCollectionItem(surveyIgdCol, data)
        if (x == False):
            return 1
    return 0

def getListRecommedationDish (rcmCol, dishCol, selectedDish):
    listRcmDish = []
    listRcm = databaseAccess.listCollectionItem(rcmCol, {}, "weight", -1)
    listRcmID = []
    for item in listRcm:
        listRcmID.append(item["dish_id"])
    totalRcmDish = [*listRcmID]
    for item in selectedDish:
        if item not in totalRcmDish:
            totalRcmDish.append(item)
    print(totalRcmDish)
    
    for item in listRcm:
        dishItem = databaseAccess.findCollectionItem(dishCol, {"id": item["dish_id"]})
        data = {
            "dish_name": dishItem["dish_name"],
            "dish_image": dishItem["dish_image"],
            "weight": item["weight"],
            "isSelected": True if item["dish_id"] in selectedDish else False
        }
        print(totalRcmDish)
        totalRcmDish.remove(item["dish_id"])
        listRcmDish.append(data)

    for id in totalRcmDish:
        dishItem = databaseAccess.findCollectionItem(dishCol, {"id": id})
        data = {
            "dish_name": dishItem["dish_name"],
            "dish_image": dishItem["dish_image"],
            "weight": 0,
            "isSelected": True
        }
        listRcmDish.append(data)

    return listRcmDish 