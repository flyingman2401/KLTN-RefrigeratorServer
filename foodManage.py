import json
import databaseAccess

    
def removeFood (mycol, data):
    item = databaseAccess.findCollectionItem(mycol, data)
    if item:
        return databaseAccess.removeCollectionItem(mycol, data)
    return False

def updateFood (mycol, data):
    filter = {
        'ingredient_id': data['ingredient_id'],
        'user_id': data['user_id'],
        'food_manufacture': data['food_manufacture'],
        'food_PRD': data['food_PRD']
    }
    return databaseAccess.updateCollectionItem(mycol, filter, {'food_amount':data['food_amount']})
        
def getFoodList (mycol):
    foodList = databaseAccess.listCollectionItem(mycol)
    return foodList

def getRecommendationList (rcmCol, dishesCol, ingredientCol):
    recommendationList = []
    recommendationInfo = databaseAccess.listCollectionItem(rcmCol)
    
    for item in recommendationInfo:
        dishItem = databaseAccess.findCollectionItem(dishesCol, {'id': item['dish_id']})
        ingredientList = []
        for ingredient in dishItem['dish_ingredients']:
            ingredientInfo = databaseAccess.findCollectionItem(ingredientCol, {'id': ingredient[0]})
            ingredientList.append(ingredientInfo['ingredient_name'])

        recommendationListItem = {
            "dish_name": dishItem['dish_name'],
            "weight": item['weight'],
            "dish_ingredients": dishItem['dish_ingredients'],
        }

        recommendationList.append(recommendationListItem)

    return recommendationList

    
    

    