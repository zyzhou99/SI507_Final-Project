from pip._vendor import requests
import random
import json

# Define the API endpoint and parameters
ingredient = input("Enter an ingredient: ")
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

# Extract the label field from each item in the "hits" array
data = [{
    "label": hit["recipe"]["label"],
    "image": hit["recipe"]["image"],
    "calories": round(hit["recipe"]["calories"]),
    "cuisineType": hit["recipe"]["cuisineType"],
    "mealType": hit["recipe"]["mealType"],
    #"healthLabels": hit["recipe"]["healthLabels"],
    "ingredientLines": hit["recipe"]["ingredientLines"]
    } for hit in response.json()["hits"]]

# Write the labels to a new JSON file
with open("recipe.json", "a") as f:
    #json.dump(data, f, indent=2)
    
    for item in data:
        json.dump(item, f, indent=2)
        f.write(",\n")
    