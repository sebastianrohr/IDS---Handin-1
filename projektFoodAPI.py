import json 
import requests

##search by ingredients
def get_recipe(*ingredients): 
    recipe_lists = []

    ingredientStr = ''
    for ingredient in ingredients:
        ingredientStr += ingredient + ","
    
    URL = "http://www.recipepuppy.com/api/?i=" + ingredientStr
    print(URL)
    getInformation = requests.get(url = URL)
    recipeInformation = getInformation.json()

    for recipe in recipeInformation['results']: 
       recipe_lists.append(recipe['title'])
    
    print(recipe_lists)

##search by query
def get_ingredients(recipe):
    URL = "http://www.recipepuppy.com/api/?q=" + recipe
    print(URL)
    getInformation = requests.get(url = URL)
    ingredientInformation = getInformation.json()

    #for ingredient in ingredientInformation['results']:
    #ingredient_list.append(ingredient['ingredients'])
    #print (ingredient_list)
    print (ingredientInformation['results'][0]['ingredients'])

##search by ingredient and query
#mangler at få til at virke med både key og query (ingredientser og ret)
#er ret sikker på at det har noget at gøre med hvordan man håndterer de forskellige inputs i funktionen. Når funktionen kaldes,
#kan den ikke finde ud af hvad der er recipe, og hvad der er ingredienser
def recipeAndIngredient(recipe, *ingredient): 
    recipe_lists = []

    ingredientStr = ''
    for ingredient in ingredients:
        ingredientStr += ingredient + ","
    
    URL = "http://www.recipepuppy.com/api/?i=" + ingredientStr + "&q=" + recipe
    print(URL)
    getInformation = requests.get(url = URL)
    recipeInformation = getInformation.json()

    for recipe in recipeInformation['results']: 
       recipe_lists.append(recipe['title'])
    
    print(recipe_lists)


#get_recipe("potato", "olive")
get_ingredients("omelet")
#recipeAndIngredient("omelet", "egg", "milk")