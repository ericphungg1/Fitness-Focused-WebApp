from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import initdb
import seng_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        jsdata = request.form['javascript_data']
        data = json.loads(jsdata)
        #should print in server terminal
        firstname = (data['fn'].replace('\xa0', '')).strip()
        email = (data['e'].replace('\xa0', '')).strip()
        password = (data['p'].replace('\xa0', '')).strip()
        print(firstname)
        print(email)
        print(password)
        #call this function
        #seng_db.newuser(firstname, lastname, email, password)
        return
    else:
        return render_template('sign-up.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/caloriecounter')
def calcount():
    food = request.args.get('food')
    Height = request.args.get('Height')
    Weight = request.args.get('Weight')
    Age = request.args.get('Age')
    Gender = request.args.get('Gender')
    if food != None: 
        food = nutrition(food)
        food_name = food["item1"]["name"]
        food_calories = food["item1"]["calories"]
        food_sodium = food["item1"]["sodium"]
        return render_template('calorie_counter.html', name=food_name, calories=food_calories, sodium=food_sodium)
    elif Height != None and Weight != None:
        BMI = Weight/(Height**2)
        return render_template('calorie_counter.html', Gender=Gender, Height=Height, Weight=Weight, Age=Age, BMI=BMI)
    else:
        return render_template('calorie_counter.html')

@app.route('/foodsearch')
def foodsearch():
    return render_template('foodsearch.html')

@app.route('/forum')
def forum():
    return render_template('community-forum.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('community-leaderboards.html')

@app.route('/fooddiary')
def fooddiary():
    return render_template('food_diary.html')

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgot-password.html')

@app.route('/homepage')
def homepage():
    return render_template('home-page.html')

@app.route('/personaltrainer')
def personaltrainer():
    return render_template('personal-trainer.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/recommendedexcercise')
def recommendedex():
    return render_template('recommended-exercise.html')

@app.route('/recommenderecipes')
def recommendedrec():
    return render_template('recommended-recipes.html')

@app.route('/rewards')
def rewards():
    return render_template('rewards.html')

def nutrition(food):
    payload = {
        "appId": 'e4d96968',
        "appKey": '4c9e97e39eafccbbf4d2fe28d3deec81',
        "fields": [
            "item_name",
            "nf_calories",
            "nf_sodium",
        ],
        "min_score": 0.5,
        "offset": 0,
        "limit": 3,
        "query": food,
    }
    res = requests.post('https://api.nutritionix.com/v1_1/search', data=payload)
    res = res.json()
    response = {
        "item1":{
            "name": res["hits"][0]["fields"]["item_name"],
            "calories": res["hits"][0]["fields"]["nf_calories"],
            "sodium": res["hits"][0]["fields"]["nf_sodium"],
        },
        "item2":{
            "name": res["hits"][1]["fields"]["item_name"],
            "calories": res["hits"][1]["fields"]["nf_calories"],
            "sodium": res["hits"][1]["fields"]["nf_sodium"],
        },
        "item3":{
            "name": res["hits"][2]["fields"]["item_name"],
            "calories": res["hits"][2]["fields"]["nf_calories"],
            "sodium": res["hits"][2]["fields"]["nf_sodium"],
        },
    }
    return response

if __name__ == '__main__':
    #initialise database
    initdb.init()
    app.run(debug=True, host='0.0.0.0')
