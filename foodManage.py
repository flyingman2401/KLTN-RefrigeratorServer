import json
import databaseAccess

def addFood (mycol, data):
    return databaseAccess.insertCollectionItem(mycol, json.loads(data))
    
def removeFood (mycol, data):
    return databaseAccess.removeCollectionItem(mycol, json.loads(data))
        
def getFoodList (mycol):
    foodList = databaseAccess.listCollectionItem(mycol)
    return foodList

def getRecommendationList (rcmCol, dishesCol):
    recommendationList = []
    recommendationInfo = databaseAccess.listCollectionItem(rcmCol)
    
    for item in recommendationInfo:
        foodItem = databaseAccess.findCollectionItem(dishesCol, {'dishname': item['dishname']})

        recommendationListItem = {
            "dishname": item['dishname'],
            "weight": item['weight'],
            "ingredients": foodItem['ingredients'],
        }

        recommendationList.append(recommendationListItem)

    return recommendationList

    
    

    