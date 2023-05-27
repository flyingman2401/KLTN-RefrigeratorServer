import databaseAccess

def getSpecificDish(igdList, dishCol):
    dishList = databaseAccess.listCollectionItem(dishCol, {})

    specificDishes = []
    for selectedigd in igdList:
        for dish in dishList:
            for igd in dish["dish_ingredients"]:
                if (igd[0] == selectedigd):
                    specificDishes.append(dish)
                    break

    print(specificDishes)
    return specificDishes

