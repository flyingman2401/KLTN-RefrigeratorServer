import json
import databaseAccess

def addFood (mycol, data):
    return databaseAccess.insertCollectionItem(mycol, json.loads(data))
    
def removeFood (mycol, data):
    return databaseAccess.removeCollectionItem(mycol, json.loads(data))
        
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
            "dishname": dishItem['dish_name'],
            "weight": item['weight'],
            "ingredients": dishItem['dish_ingredients'],
        }

        recommendationList.append(recommendationListItem)

    return recommendationList

    
    

    