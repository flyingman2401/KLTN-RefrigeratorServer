import databaseAccess

def getDishInfo (dishCol, ingredientCol, typeCol, id):
    dishItem = databaseAccess.findCollectionItem(dishCol, {'id': id})

    for ingredient in dishItem['dish_ingredients']:
        ingredientItem = databaseAccess.findCollectionItem(ingredientCol, {'id': ingredient[0]})
        ingredient.append(ingredientItem['ingredient_name'])
        ingredient.append(ingredientItem['ingredient_nutrion'])

    dishType = databaseAccess.findCollectionItem(typeCol, {'id': dishItem['dishtype_id']})

    dishInfo = {
        "dish_id": dishItem['id'],
        "dish_name": dishItem['dish_name'],
        "dish_ingredients": dishItem['dish_ingredients'],
        "dish_image": dishItem['dish_image'],
        "dishtype_id": dishItem['dishtype_id'],
        "type_name": dishType['type_name']
    }

    return dishInfo

def removeIngredient (mycol, data):
    item = databaseAccess.findCollectionItem(mycol, data)
    if item:
        return databaseAccess.removeCollectionItem(mycol, data)
    return False

def updateIngredient (mycol, data):
    filter = {
        'ingredient_id': data['ingredient_id'],
        'user_id': data['user_id'],
        'food_manufacture': data['food_manufacture'],
        'food_PRD': data['food_PRD']
    }
    return databaseAccess.updateCollectionItem(mycol, filter, {'food_amount':data['food_amount']})
        
def getListIngredientInsideFridge (igdInsideCol, igdCol):
    listIngredient = databaseAccess.listCollectionItem(igdInsideCol, {})
    for item in listIngredient:
        itemdetail = databaseAccess.findCollectionItem(igdCol, {"id": item['ingredient_id']})
        item['ingredient_name'] = itemdetail['ingredient_name']
        item['ingredient_image'] = itemdetail['ingredient_image']
        item['ingredient_nutrion'] = itemdetail['ingredient_nutrion']
    return listIngredient

def getListRecommedationDish (rcmCol, dishCol, ingredientCol, typeCol):
    listRcmDish = []
    listRcm = databaseAccess.listCollectionItem(rcmCol, {})
    
    for item in listRcm:
        dishItem = getDishInfo(dishCol, ingredientCol, typeCol, item['dish_id'])
        dishItem['weight'] = item['weight']
        listRcmDish.append(dishItem)

    return listRcmDish

def getListRecommedationMeal (rcmCol, dishCol, ingredientCol, typeCol):
    listRcmMeal = []
    listRcm = databaseAccess.listCollectionItem(rcmCol, {})

    for item in listRcm:
        dishInfo = []
        dishID = item['id'].split("_")

        for id in dishID:
            dishItem = getDishInfo(dishCol, ingredientCol, typeCol, id)
            dishInfo.append(dishItem)

        mealItem = {
            "dish": dishInfo,
            "weight": item['weight']
        }
        listRcmMeal.append(mealItem)

    return listRcmMeal    

def rateDish (mycol, data):
    filter = {
        'user_id': data['user_id'],
        'dish_id': data['dish_id']
    }
    rateInfo = databaseAccess.findCollectionItem(mycol, filter)
    if not rateInfo:
        x = databaseAccess.insertCollectionItem(mycol, data)
        return x
    else:
        x = databaseAccess.updateCollectionItem(mycol, filter, {'rating': data['rating']})
        return x
