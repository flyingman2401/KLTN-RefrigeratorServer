import databaseAccess

def getSpecificDish(igdList, dishCol):
    dishList = databaseAccess.listCollectionItem(dishCol, {})

    specificDishes = []
    for selectedigd in igdList:
        for dish in dishList:
            for igd in dish["dish_ingredients"]:
                if (igd[0] == selectedigd):
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
            "ingredient_unit": igd["ingredient_unit"]
        }
        igdList.append(data)
    return igdList
