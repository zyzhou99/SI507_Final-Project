from pip._vendor import requests
import json

def get_recipe_data(ingredient):
    url = "https://api.edamam.com/api/recipes/v2"
    params = {
        "q": ingredient,
        "type": "public",
        "app_id": "8dd54645",
        "app_key": "50580ed94f36ce3cd0227bfee7e99718",
        "from": 0,
        "to": 100,
    }
    response = requests.get(url, params=params)

    with open('json/cache.json', 'r') as f:
        data = json.load(f)

    new_data = {item["recipe"]["label"]: {
                "name": item["recipe"]["label"],
                "image": item["recipe"]["image"],
                "calories": round(item["recipe"]["calories"]),
                "cuisineType": item["recipe"]["cuisineType"],
                "mealType": item["recipe"]["mealType"],
                "ingredientLines": item["recipe"]["ingredientLines"]
            } for item in response.json()["hits"]}

    data.update(new_data)

    with open("json/cache.json", "w") as f:
        json.dump(data, f, indent=2)

def get_exercise_data(activity):
    url='https://trackapi.nutritionix.com/v2/natural/exercise'
    headers = {
        "x-app-id": "ce50cb8a",
        "x-app-key": "23ab83e7ce98ac4d9ca3df633a91d0b9",
        "Content-Type" : "application/json"
    }
    input = {'query': activity}

    response = requests.post(url, headers=headers, json=input)

    with open('json/exercise_cache.json', 'r') as f:
        data = json.load(f)

    new_data = { item['name']:{
                "name":item['name'],
                "MET": item['met'],
                "calories per min": round(item['nf_calories'] / (item['duration_min']+1), 2),
            } for item in response.json()["exercises"]}
    data.update(new_data)

    with open("json/exercise_cache.json", "w") as f:
        json.dump(data, f, indent=2)

    return new_data
