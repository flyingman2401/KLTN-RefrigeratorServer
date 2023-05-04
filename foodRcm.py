import databaseAccess
from datetime import datetime    

def calculateIgdWeight(neededIgdList, igdInsideFridgeList):
    weightIngredient = 0
    hasImportantIgd = False
    
    # Check if ingredients is available in refrigerator
    for ingredientOfDish in neededIgdList:
            
        for igd in igdInsideFridgeList:
            if (ingredientOfDish[0]) == igd['ingredient_id']:

                # If the most important ingredient is available in refrigerator
                if (ingredientOfDish[0] == neededIgdList[0][0]):
                    hasImportantIgd = True
                
                expDate = datetime.strptime(igd['food_EXP'], '%Y-%m-%d').date()
                today = datetime.now().date()
                remainingDays = (expDate - today).days

                if (remainingDays <= -5):
                    weightEXP = 0
                elif (remainingDays > 10):
                    weightEXP = 0.05
                elif (remainingDays > 0):
                    weightEXP = (1.1 - remainingDays/10)
                else:
                    weightEXP = 1

                # Update the weight of ingredient for this dish
                weightIngredient += ingredientOfDish[3] * weightEXP 
                break       
        
        if hasImportantIgd == False:
            return 0
        
    return weightIngredient

def calculateRatingWeight(dishID, userID, ratingCol):
    ratingInfo = databaseAccess.findCollectionItem(ratingCol, {"user_id": userID, "dish_id": dishID})
    if ratingInfo:
        weightRating = ratingInfo['rating']
    else:
        weightRating = 1
    return weightRating

def updateIgdWeight(dishCol, dishID, mealIgd):
    igdList = databaseAccess.findCollectionItem(dishCol, {"id": dishID})['dish_ingredients']
    for ingredient in igdList:
        weightIngredient = ingredient[3] / 3
        for appendedIgd in mealIgd:
            if (ingredient[0] == appendedIgd[0]):
                appendedIgd[1] += weightIngredient
                return
        mealIgd.append([ingredient[0], ingredient[1], ingredient[2], weightIngredient])

def updateRcmDish(dishCol, igdInsideFridgeCol, rcmDishCol, ratingCol, userID):
    dishList = databaseAccess.listCollectionItem(dishCol, {})
    igdInsideFridgeList = databaseAccess.listCollectionItem(igdInsideFridgeCol, {'user_id': userID})

    databaseAccess.emptyCollection(rcmDishCol, {'user_id': userID})

    for dish in dishList:
        weightIngredient = calculateIgdWeight(dish['dish_ingredients'], igdInsideFridgeList)
        weightRating = calculateRatingWeight(dish['id'], userID, ratingCol)

        if (weightIngredient > 0):
            
            weightDish = 0.7 * weightIngredient + 0.3 * weightRating

            jsonData = {
                "dish_id": dish['id'],
                "user_id": userID,
                "weight": round(weightDish, 5)
            }
            print(jsonData)

            databaseAccess.insertCollectionItem(rcmDishCol, jsonData)

def updateRcmMeal(dishCol, igdInsideFridgeCol, rcmDishCol, rcmMealCol, ratingCol, userID):
    recommendedMeal = [[],[],[]]
    recommendedDishList = databaseAccess.listCollectionItem(rcmDishCol, {'user_id': userID})
    igdInsideFridgeList = databaseAccess.listCollectionItem(igdInsideFridgeCol, {'user_id': userID})

    # Classify recommendation dishes into 3 different dishtype array
    for recommendedDish in recommendedDishList:
        dishType = databaseAccess.findCollectionItem(dishCol, {"id": recommendedDish['dish_id']})['dishtype_id']
        recommendedMeal[dishType].append(recommendedDish['dish_id'])

    igdOfMeals = {}
    databaseAccess.emptyCollection(rcmMealCol, {'user_id': userID})

    # Check if enough condition to recommend meals
    if (len(recommendedMeal[0]) == 0 or len(recommendedMeal[1]) == 0 or len(recommendedMeal[2]) == 0):
        print("Không đủ gợi ý món ăn để tạo thành bữa ăn")
        return

    # Update weight of ingredient for recommended meals
    for monCanh in recommendedMeal[0]:
        for monKho in recommendedMeal[1]:
            for monXao in recommendedMeal[2]:
                mealIgd = []
                updateIgdWeight(dishCol, monCanh, mealIgd)
                updateIgdWeight(dishCol, monKho, mealIgd)
                updateIgdWeight(dishCol, monXao, mealIgd)
                mealID = monCanh + '-' + monKho + '-' + monXao
                igdOfMeals[mealID] = mealIgd

    # Calculate the weight for each recommended meal
    for mealID, mealIgd in igdOfMeals.items():
        weightIngredient = calculateIgdWeight(mealIgd, igdInsideFridgeList)

        dishIDs = mealID.split('-')
        weightRating = 0
        for dishID in dishIDs:
            weightRating += calculateRatingWeight(dishID, userID, ratingCol)
        weightRating /= 3

        weightMeal = 0.7 * weightIngredient + 0.3 * weightRating

        jsonData = {
            "meal_id": mealID,
            "user_id": userID,
            "weight": round(weightMeal, 5)
        }
        print(jsonData)

        databaseAccess.insertCollectionItem(rcmMealCol, jsonData)
