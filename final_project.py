from pip._vendor import requests
import tree
import json
import getData
from flask import Flask, render_template

app = Flask(__name__)

edamam_url="https://api.edamam.com/api/recipes/v2?type=public&app_id=8dd54645&app_key=50580ed94f36ce3cd0227bfee7e99718"

cuisineList=tree.treeGroups["cuisineType"];
cook=""
cuisine=""
ingredients=""
goal_intake=0
consume_calories=0
exercise_calorie=0
calorie=0
sportList=[]
cuisine_bl = False
cook_bl=False
ingredients_bl=False
goal_intake_bl=False
consume_calories_bl=False
exercise_calorie_bl=False
recoomnd_list=[]
reco_recipe_list=[]
recoomnd_len=5


def ask_cuisine():
    global cuisine,cuisine_bl,cuisineList
    if cuisine_bl==False:
        print("2.What cuisine are you craving?")
        print("(eg:" + ','.join(cuisineList)+")")
        cuisine = input()
        for str in cuisineList:
            if cuisine.lower() == str:
                cuisine_bl = True

def ask_ingredients():
    global ingredients, ingredients_bl
    if ingredients_bl==False:
        print("3.What are the main ingredients you have in your fridge?")
        ingredients = input()
        response = requests.get(edamam_url+"&q="+ingredients)
        response=response.json()
        if response.get("count")>0:
            ingredients_bl=True
        else:
            ingredients_bl=False

def ask_intake_goal():
    global goal_intake,goal_intake_bl
    if goal_intake_bl==False:
        print("4.What is your caloric intake goal for today?")
        num=input()
        if num.isdigit() and int(num)>0:
            goal_intake=int(num)
            goal_intake_bl=True
        else:
            print("The number of intake goal must be greater than 0!")
            ask_intake_goal()

def ask_calories_consume():
    global consume_calories,consume_calories_bl
    if consume_calories_bl==False:
        print("5.How many calories did you consume already?")
        num=input()
        if num.isdigit() and int(num)>0:
            consume_calories=int(num)
            consume_calories_bl=True
        else:
            print("The number of consume calories must be greater than 0!")
            ask_intake_goal()

def ask_exercise_calorie_child():
    global exercise_calorie, exercise_calorie_bl,sportList
    print("-----The following sport has been queried, please select the sport you want to play:")
    sportName=""
    for sport in sportList:
        sportName+="{ name:"+sport.get("name")+",calories per min:"+str(sport.get("calories per min"))+"} "
    print("----------"+str(sportName))
    now_sport=input()
    now_bl=False
    for sport in sportList:
        if sport.get("name").lower()==now_sport.lower():
            now_bl=True
            print("-----Please enter how long you want to exercise (in minutes):")
            now_min=input()
            exercise_calorie = int(sport.get("calories per min")*float(now_min))
    if now_bl:
        exercise_calorie_bl=True
    else:
        print("Please enter the correct sport name!")
        ask_exercise_calorie_child()


def ask_exercise_calorie():
    global sportList,exercise_calorie_bl
    if exercise_calorie_bl==False:
        print("6.What exercise are you going to do today?")
        sport=input()
        with open('json/exercise_cache.json', 'r') as f:
            data_list = json.load(f)
            for data in data_list:
               if sport in data:
                   sportList.append(data_list[data])
            if len(sportList)==0:
                sport_api=getData.get_exercise_data(sport)
                if len(sport_api)>0:
                    sportList.append(sport_api)
                    ask_exercise_calorie()
                else:
                    print("Cannot query the current motion, please enter again!")
                    ask_exercise_calorie()
            else:
                ask_exercise_calorie_child()


def recoomd():
    global cook,cuisine,ingredients,recoomnd_list,recoomnd_len,consume_calories,\
    exercise_calorie,goal_intake,calorie
    if cook.lower() == "breakfast":
        calorie=((int(goal_intake)+int(exercise_calorie)-int(consume_calories))/3)
    elif cook.lower() == "lunch":
        calorie=((int(goal_intake)+int(exercise_calorie)-int(consume_calories))/2)
    elif cook.lower() == "dinner":
        calorie=((int(goal_intake)+int(exercise_calorie)-int(consume_calories))/1)
    #print(calorie)

    min_calorie=calorie-1
    max_calorie=calorie+1

    #meal_food_list=getMealList(cook)
    cuisine_food_list=getCuisineList(cuisine)
    calorie_food_list=getCalorieList(calorie)
    food_list=[]
    recoomnd_list=[]

    #for meal_food in meal_food_list:
    for cuisine_food in cuisine_food_list:
        for calorie_food in calorie_food_list:
            if cuisine_food.lower() == calorie_food.lower():
                food_list.append(cuisine_food)

    for food in food_list:
        if ingredients in food.lower():
            recoomnd_list.append(food)

    if len(recoomnd_list)==0:
        add_recipe_data(ingredients)

        #meal_food_list = getMealList(cook)
        cuisine_food_list = getCuisineList(cuisine)
        calorie_food_list = getCalorieList(calorie)
        food_list = []
        recoomnd_list = []

        #for meal_food in meal_food_list:
        for cuisine_food in cuisine_food_list:
            for calorie_food in calorie_food_list:
                if cuisine_food.lower() == calorie_food.lower():
                    food_list.append(cuisine_food)

        for food in food_list:
            if ingredients in food.lower():
                recoomnd_list.append(food)

def add_recipe_data(ingredient):
    getData.get_recipe_data(ingredient)
    tree.add()


def getCuisineList(cuisine):
    cuisine_tree=tree.loadTree("json/cuisineType.json")
    cuisine_list=tree.FindNode(cuisine_tree,cuisine).reipes
    return cuisine_list

def getCalorieList(calorie):
    calorie_tree=tree.loadTree("json/calories.json")
    now_calorie_interval=""
    for calorie_interval in calorie_tree.groups:
        if float(calorie_interval.split('-')[0]) <= float(calorie) < float(calorie_interval.split('-')[1]):
            now_calorie_interval=calorie_interval
            break
    calorie_list = tree.FindNode(calorie_tree, now_calorie_interval).reipes
    return calorie_list


def reco_recipe():
    with open('json/cache.json') as f:
        data = json.load(f)
    for i in recoomnd_list:
        if i in data:
            reco_recipe_list.append(data[i])
        else:
            print('Sorry, we can not find any dish that fits your requirement')
    return reco_recipe_list

@app.route("/")
def index():
    data = reco_recipe_list
    return render_template('index.html', data=data)

def enquire():
    global cook, cook_bl, cuisine, cuisine_bl,ingredients,ingredients_bl, \
        allergies,num_ingredients,goal_intake,goal_intake_bl, \
        consume_calories,consume_calories_bl,exercise_calorie, exercise_calorie_bl,calorie
    if cook_bl == False:
        print("1.Which meal are you trying to cook? (Breakfast, lunch, or dinner)")
        cook = input()
        cook = cook.lower()

    if cook != "dinner" and cook != "lunch" and cook != "breakfast":
        print("Please enter the correct cook name!")
        enquire()
    else:
        cook_bl = True
        ask_cuisine()
        if cuisine_bl:
            ask_ingredients()
            if ingredients_bl:
                ask_intake_goal()
                if goal_intake_bl:
                    ask_calories_consume()
                    if consume_calories_bl:
                        ask_exercise_calorie()
                        if exercise_calorie_bl:
                            recoomd()
                            reco_recipe()
                            print("Check out your recommended recipes in the link below:")
                            app.run()
            else:
                print("The element cannot be found!")
                enquire()
        else:
            print("This cuisine is not found!")
            enquire()

enquire()