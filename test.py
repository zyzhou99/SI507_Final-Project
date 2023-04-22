from pip._vendor import requests
import json
import getData
from flask import Flask, render_template

recoomnd_list = ['Chicken Vesuvio', 'Chicken Paprikash']
reco_recipe_list = []

app = Flask(__name__)

def reco_recipe():
    with open('json/cache.json') as f:
        data = json.load(f)
    for i in recoomnd_list:
        if i in data:
            reco_recipe_list.append(data[i])
        else:
            print('none')
    return reco_recipe_list
reco_recipe()

def result():
    for i in reco_recipe_list:
        return f"The recommended dish is {i['name']}"

#print(result())

@app.route("/")
def index():
    data = reco_recipe_list
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run()