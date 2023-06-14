import databaseAccess
import datetime
import pytz

def RecommendDishes(now, userID):
    databaseAccess.emptyCollection(collectionList['RecommendationDish'], {})
    dishList = databaseAccess.listCollectionItem(collectionList['Dish'], {})
    ingredientIFList_ID = databaseAccess.getColumnInCollection(collectionList['IngredientInsideFridge'], 'ingredient_id', {"user_id": userID})
  
    # Traverse the ingredients of all over dishes
    for dish in dishList:
        weightIngredient = 0
        expiredIngredients = []
        # Check if the most important ingredient is available in refrigerator
        if (dish['dish_ingredients'][0][0] in ingredientIFList_ID):
            # Traverse the ingredients of a dish
            for ingredientOfDish in dish['dish_ingredients']:
                # Check if this ingredient is available in refrigerator
                if (ingredientOfDish[0] in ingredientIFList_ID):
                    ingredientInfo = databaseAccess.findCollectionItem(collectionList['IngredientInsideFridge'], {"user_id": userID, "ingredient_id": ingredientOfDish[0]})
                    # Calculate the weight of exp
                    expDate = datetime.datetime.strptime(ingredientInfo['food_EXP'], '%Y-%m-%d').date()
                    prdDate = datetime.datetime.strptime(ingredientInfo['food_PRD'], '%Y-%m-%d').date()
                    today = now.date()

                    totalUseDays = (expDate - prdDate).days - 1
                    remainingDays = (expDate - today).days

                    # Nếu thực phẩm đã hết hạn thì cho weightEXP = 0 để trừ trọng số của thực phẩm đó ra khỏi món ăn
                    if (remainingDays < 0):
                        weightEXP = 0
                        expiredIngredients.append(ingredientOfDish[0])
                    # Ngày hết hạn
                    elif (remainingDays < 1):
                        weightEXP = 1
                    # Trước ngày hết hạn
                    else:
                        weightEXP = (totalUseDays - remainingDays + 1)/totalUseDays

                    # Update the weight of ingredient for this dish
                    weightIngredient += ingredientOfDish[2] * weightEXP
                    print(ingredientOfDish[0], weightIngredient, weightEXP)

        # Get rating record from user ID and dish ID
        ratingInfo = databaseAccess.findCollectionItem(collectionList['Rating'], {"user_id": userID, "dish_id": dish['id']})
        if (ratingInfo == None):
            ratingInfo = {
                "rating": 0
            }

        # Calculate final weight of recommended dish
        weightDish = 0.7 * weightIngredient + 0.3 * ratingInfo['rating']
        print(weightIngredient)
        if (weightIngredient > 0):
            jsonData = {
                "dish_id": dish['id'],
                "user_id": userID,
                "weight": round(weightDish, 3)
            }
            print(jsonData)
            # print(expiredIngredients)

            databaseAccess.insertCollectionItem(collectionList['RecommendationDish'], jsonData)

def GetNeededIngredientsOfMeals(now, userID):
    recommendedMeal = [[],[],[],[],[]]
    recommendedDishList = databaseAccess.listCollectionItem(collectionList['RecommendationDish'], {"user_id": userID})
    
    for recommendedDish in recommendedDishList:
        # Get dish type of this recommended dish
        DishType = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": recommendedDish['dish_id']})['dishtype_id']
        # Distribute each type of dish to the corresponding list
        recommendedMeal[DishType].append(recommendedDish['dish_id'])

    neededIngredientsOfMeals = {}

    hourNow = now.hour
    # Recommend for recommended breakfast (21 <= hourNow < 9):
    if (hourNow < morningNoticeHour or hourNow >= eveningNoticeHour):
        # Nếu có thức uống có thể làm được trong buổi sáng
        if (recommendedMeal[4]):
            for monAnSang in recommendedMeal[3]:
                for thucUong in recommendedMeal[4]:
                    neededIngredients = []
                    monAnSangIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": monAnSang})['dish_ingredients']
                    thucUongIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": thucUong})['dish_ingredients']

                    for ingredient in monAnSangIngredients:
                        weightIngredient = ingredient[2] * 0.7
                        neededIngredients.append([ingredient[0], weightIngredient])

                    for ingredient in thucUongIngredients:
                        weightIngredient = ingredient[2] * 0.3
                        if (ingredient[0] not in [i[0] for i in neededIngredients]):
                            neededIngredients.append([ingredient[0], weightIngredient])
                        else:
                            for index, neededIngredient in enumerate(neededIngredients):
                                if ingredient[0] in neededIngredient:
                                    neededIngredients[index][1] += weightIngredient

                    mealID = monAnSang + '-' + thucUong
                    neededIngredientsOfMeals[mealID] = neededIngredients

            return neededIngredientsOfMeals
        
        for monAnSang in recommendedMeal[3]:
            neededIngredients = []
            monAnSangIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": monAnSang})['dish_ingredients']
            for ingredient in monAnSangIngredients:
                neededIngredients.append([ingredient[0], ingredient[2]])

            mealID = monAnSang
            neededIngredientsOfMeals[mealID] = neededIngredients

        return neededIngredientsOfMeals

    # Update weight of ingredient for other recommended meals
    for monCanh in recommendedMeal[0]:
        for monChinh in recommendedMeal[1]:
            for monPhu in recommendedMeal[2]:
                neededIngredients = []
                monCanhIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": monCanh})['dish_ingredients']
                monChinhIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": monChinh})['dish_ingredients']
                monPhuIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": monPhu})['dish_ingredients']
                for ingredient in monCanhIngredients:
                    weightIngredient = ingredient[2] / 3
                    neededIngredients.append([ingredient[0], weightIngredient])

                for ingredient in monChinhIngredients:
                    weightIngredient = ingredient[2] / 3
                    if (ingredient[0] not in [i[0] for i in neededIngredients]):
                        neededIngredients.append([ingredient[0], weightIngredient])
                    else:
                        for index, neededIngredient in enumerate(neededIngredients):
                            if ingredient[0] in neededIngredient:
                                neededIngredients[index][1] += weightIngredient

                for ingredient in monPhuIngredients:
                    weightIngredient = ingredient[2] / 3
                    if (ingredient[0] not in [i[0] for i in neededIngredients]):
                        neededIngredients.append([ingredient[0], weightIngredient])
                    else:
                        for index, neededIngredient in enumerate(neededIngredients):
                            if ingredient[0] in neededIngredient:
                                neededIngredients[index][1] += weightIngredient
                
                mealID = monCanh + '-' + monChinh + '-' + monPhu
                neededIngredientsOfMeals[mealID] = neededIngredients
    
    return neededIngredientsOfMeals

def CalculateIngredientWeight(now, neededIngredientsOfMeal, ingredientIFList_ID, userID):
    weightIngredient = 0
    chosenIngredientList = []
    expiredIngredients = []
    for neededIngredients in neededIngredientsOfMeal:
        if (neededIngredients[0] in ingredientIFList_ID):
            ingredientInfo = databaseAccess.findCollectionItem(collectionList['IngredientInsideFridge'], {"user_id": userID, "ingredient_id": neededIngredients[0]})
            # Calculate the weight of exp
            expDate = datetime.datetime.strptime(ingredientInfo['food_EXP'], '%Y-%m-%d').date()
            prdDate = datetime.datetime.strptime(ingredientInfo['food_PRD'], '%Y-%m-%d').date()
            today = now.date()

            totalUseDays = (expDate - prdDate).days - 1
            remainingDays = (expDate - today).days

            # Nếu thực phẩm đã sau hết hạn thì cho weightEXP = 0 để trừ trọng số của thực phẩm đó ra khỏi món ăn
            if (remainingDays < 0):
                weightEXP = 0
                expiredIngredients.append(neededIngredients[0])
            # Ngày hết hạn
            elif (remainingDays == 0):
                weightEXP = 1
            # Trước ngày hết hạn
            else:
                weightEXP = (totalUseDays - remainingDays + 1)/totalUseDays

            # Update the weight of ingredient for this dish
            weightIngredient += neededIngredients[1] * weightEXP
            # Append this ingredient to chosenIngredientList
            chosenIngredientList.append(neededIngredients[0])

    return round(weightIngredient, 5), chosenIngredientList, expiredIngredients

def CalculateDiseaseWeight(now, userID, dishIDs):
    # X2 = w_h + w_uh
    # Where:
    # 	w_h = 1/3 * N_h
    # 	w_uh = - (1/3 * N_uh)

    userInfo = databaseAccess.findCollectionItem(collectionList['User'], {"id": userID})
    # Nếu user không có bệnh thì trọng số bằng 1
    if (not userInfo["user_disease"]):
        return 1, []

    diseaseInfo = databaseAccess.findCollectionItem(collectionList['Disease'], {"id": userInfo["user_disease"]})
    healthyDishes = diseaseInfo['disease_healthy_dish']
    unhealthyDishes = diseaseInfo['disease_unhealthy_dish']
    
    unhealthyDishesInMeal = []
    numHealthyDish, numUnhealthyDish = 0, 0
    for dish in dishIDs:
        if (dish in healthyDishes):
            numHealthyDish += 1
        elif (dish in unhealthyDishes):
            numUnhealthyDish += 1
            unhealthyDishesInMeal.append(dish)

    # Nếu là buổi sáng thì chia 2, các buổi khác chia 3
    if (now.hour < morningNoticeHour or now.hour >= eveningNoticeHour):
        weightDisease = (numHealthyDish / 2) - (numUnhealthyDish / 2)
    else:
        weightDisease = (numHealthyDish / 3) - (numUnhealthyDish / 3)
    
    return weightDisease, unhealthyDishesInMeal

def CalculateNutrientWeight(now, userInfo, dishIDs, chosenIngredientList):
    # X3 = w1 * (1 - |calories - calories_ideal| / calories_ideal) 
    #    + w2 * (1 - |protein - protein_ideal| / protein_ideal) 
    #    + w3 * (1 - |carbohydrates - carbohydrates_ideal| / carbohydrates_ideal) 
    #    + w4 * (1 - |fat - fat_ideal| / fat_ideal)
    #    + w5 * (1 - |fiber - fiber_ideal| / fiber_ideal)
    weightNutrient = 0
    # Biến lưu toàn bộ nguyên liệu cần cho một bữa ăn cùng với tổng khối lượng của chúng
    ingredientNeededForMeal = {}
    for dishID in dishIDs:
        DishIngredients = databaseAccess.findCollectionItem(collectionList['Dish'], {"id": dishID})['dish_ingredients']
        for DishIngredient in DishIngredients:
            if (DishIngredient[0] not in ingredientNeededForMeal):
                ingredientNeededForMeal[DishIngredient[0]] = DishIngredient[1]
            else:
                ingredientNeededForMeal[DishIngredient[0]] += DishIngredient[1]
    
    # Calculate sum of calories in chosenIngredientList
    calories, protein, carb, fat, fiber = 0, 0, 0, 0, 0
    chosenIngredientWithMassList = {}
    for ingredient in chosenIngredientList:
        ingredientInsideFridgeInfo = databaseAccess.findCollectionItem(collectionList['IngredientInsideFridge'], {"user_id": userInfo['id'], "ingredient_id": ingredient})
        ingredientInfo = databaseAccess.findCollectionItem(collectionList['Ingredient'], {"id": ingredient})

        # If: khối lượng thực phẩm hiện có < khối lượng thực phẩm cần => khối lượng lấy ra = khối lượng thực phẩm hiện có
        ingredientNeeded_amount = ingredientNeededForMeal[ingredient]
        if (ingredientInsideFridgeInfo['food_amount'] < ingredientNeeded_amount):
            mass = ingredientInsideFridgeInfo['food_amount']
        else:
            mass = ingredientNeeded_amount

        chosenIngredientWithMassList[ingredient] = mass

        # Calculate actual calories
        if (ingredientInfo['ingredient_unit'] == 'gram' or ingredientInfo['ingredient_unit'] == 'ml'):
            calories += (ingredientInfo['ingredient_kcal']/100  * mass)
            protein += (ingredientInfo['ingredient_protein']/100  * mass)
            carb += (ingredientInfo['ingredient_carb']/100  * mass)
            fat += (ingredientInfo['ingredient_fat']/100  * mass)
            fiber += (ingredientInfo['ingredient_fiber']/100  * mass)
        else:
            calories += (ingredientInfo['ingredient_kcal'] * mass)
            protein += (ingredientInfo['ingredient_protein'] * mass)
            carb += (ingredientInfo['ingredient_carb'] * mass)
            fat += (ingredientInfo['ingredient_fat'] * mass)
            fiber += (ingredientInfo['ingredient_fiber'] * mass)
        # print(ingredient, mass, calories, protein, carb, fat, fiber)

    calories_ideal = userInfo['user_ideal_kcal']
    protein_ideal = (userInfo['user_ideal_protein'][0] + userInfo['user_ideal_protein'][1]) / 2
    carb_ideal = (userInfo['user_ideal_carb'][0] + userInfo['user_ideal_carb'][1]) / 2
    fat_ideal = (userInfo['user_ideal_fat'][0] + userInfo['user_ideal_fat'][1]) / 2
    fiber_ideal = userInfo['user_ideal_fiber']

    hourNow = now.hour
    # Nutrient ideal for morning (21 <= hourNow < 9): 30-35% of daily calories for breakfast
    if (hourNow < morningNoticeHour or hourNow >= eveningNoticeHour):
        calories_ideal_session = calories_ideal * 0.325
        protein_ideal_session = protein_ideal * 0.325
        carb_ideal_session = carb_ideal * 0.325
        fat_ideal_session = fat_ideal * 0.325
        fiber_ideal_session = fiber_ideal * 0.325
    # Nutrient ideal for afternoon (9 <= hourNow < 14): 35-40% of daily calories for lunch
    elif (hourNow < afternoonNoticeHour): 
        calories_ideal_session = calories_ideal * 0.375
        protein_ideal_session = protein_ideal * 0.375
        carb_ideal_session = carb_ideal * 0.375
        fat_ideal_session = fat_ideal * 0.375
        fiber_ideal_session = fiber_ideal * 0.375
    # Nutrient ideal for evening (14 <= hourNow < 21): 25-35% of daily calories for dinner
    else:
        calories_ideal_session = calories_ideal * 0.3
        protein_ideal_session = protein_ideal * 0.3
        carb_ideal_session = carb_ideal * 0.3
        fat_ideal_session = fat_ideal * 0.3
        fiber_ideal_session = fiber_ideal * 0.3

    calories_deviation = calories - calories_ideal_session
    protein_deviation = protein - protein_ideal_session
    carb_deviation = carb - carb_ideal_session
    fat_deviation = fat - fat_ideal_session
    fiber_deviation = fiber - fiber_ideal_session

    actualNutrient = [calories, protein, carb, fat, fiber]
    # if (dishIDs[1] == 'DISH026'):
    #     print(dishIDs)
    #     print(int(calories_deviation), int(protein_deviation), int(carb_deviation), int(fat_deviation), int(fiber_deviation))

    weightNutrient = (0.2 * (1 - (abs(calories_deviation) / calories_ideal_session)) 
                    + 0.2 * (1 - (abs(protein_deviation) / protein_ideal_session))
                    + 0.2 * (1 - (abs(carb_deviation) / carb_ideal_session))
                    + 0.2 * (1 - (abs(fat_deviation) / fat_ideal_session))
                    + 0.2 * (1 - (abs(fiber_deviation) / fiber_ideal_session))
                    )

    return round(weightNutrient, 5), actualNutrient, chosenIngredientWithMassList

def CalculateRatingWeight(now, dishIDs, userID):
    weightRating = 0
    for dishID in dishIDs:
        ratingInfo = databaseAccess.findCollectionItem(collectionList['Rating'], {"user_id": userID, "dish_id": dishID})
        if (ratingInfo == None):
            ratingInfo = {
                "rating": 0
            }
        weightRating += ratingInfo['rating']
    
    # Nếu là buổi sáng thì chia 2, các buổi khác chia 3
    if (now.hour < morningNoticeHour or now.hour >= eveningNoticeHour):
        weightRating /= 2
    else:
        weightRating /= 3

    return round(weightRating, 5)

def RecommendMeals(now, userID):
    databaseAccess.emptyCollection(collectionList['RecommendationMeal'], {})
    userInfo = databaseAccess.findCollectionItem(collectionList['User'], {"id": userID})
    ingredientIFList_ID = databaseAccess.getColumnInCollection(collectionList['IngredientInsideFridge'], 'ingredient_id', {"user_id": userID})
    neededIngredientsOfMeals = GetNeededIngredientsOfMeals(now, userID)
    
    mealInfos = {}
    # Calculate the weight for each recommended meal
    for mealID, neededIngredientsOfMeal in neededIngredientsOfMeals.items():
        dishIDs = mealID.split('-')

        # Weight ingredient
        weightIngredient, chosenIngredientList, expiredIngredients = CalculateIngredientWeight(now, neededIngredientsOfMeal, ingredientIFList_ID, userID)

        # Weight disease
        weightDisease, unhealthyDishesInMeal = CalculateDiseaseWeight(now, userID, dishIDs)
        
        # Weight nutrient
        weightNutrient, actualNutrient, chosenIngredientWithMassList = CalculateNutrientWeight(now, userInfo, dishIDs, chosenIngredientList)

        # Example:
        # expiredIngredients           : ['VEG026']
        # actualNutrient               : [430.0, 41.74999999999999, 27.5, 22.349999999999998, 7.45]
        # chosenIngredientWithMassList : {'MEA004': 100, 'MEA007': 100, 'VEG023': 50, 'VEG024': 50, 'VEG026': 200, 'VEG007': 200}
        
        # weight rating
        weightRating = CalculateRatingWeight(now, dishIDs, userID)
        print(weightIngredient, chosenIngredientList, expiredIngredients)
        print(weightDisease, unhealthyDishesInMeal)
        print(weightNutrient, actualNutrient, chosenIngredientWithMassList)
        print(weightRating)
        # Final weight of recommended meal
        weightMeal = 0.5 * weightIngredient + 0.2 * weightDisease + 0.2 * weightNutrient +  0.1 * weightRating
        print(weightMeal)

        if (weightMeal > 0):
            mealInfos[mealID] = {
                'expiredIngredients': expiredIngredients,
                'actualNutrient': actualNutrient,
                'chosenIngredientWithMassList': chosenIngredientWithMassList
            }

            jsonData = {
                "meal_id": mealID,
                "user_id": userID,
                "weight": round(weightMeal, 3),
                "meal_unhealthy_dishes": unhealthyDishesInMeal,
                "meal_nutrient": actualNutrient
            }
            print(jsonData)
            databaseAccess.insertCollectionItem(collectionList['RecommendationMeal'], jsonData)
        else:
            print("Không đủ nguyên liệu để tạo thành bữa ăn!")

    return mealInfos

morningNoticeHour = 9
afternoonNoticeHour = 14
eveningNoticeHour = 21
timezone = pytz.timezone('Asia/Ho_Chi_Minh')

collectionList = {
    "User": "",
    "Device": "",
    "SensorsData": "",
    "Rating": "",
    "Dish": "",
    "Ingredient": "",
    "DishType": "",
    "IngredientInsideFridge": "", 
    "RecommendationDish": "",
    "RecommendationMeal": "",
    "Disease": "",
    "History": ""
}