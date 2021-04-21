from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import initdb
import seng_db
import urllib.request
import re
app = Flask(__name__)
import smtplib 

def sendemail():
    email = smtplib.SMTP('smtp.gmail.com', 587) 
    email.starttls() 
    email.login("sengsmartbite@gmail.com", "ILOVESENG") 
    message = "Claim your Free Gym Gear Voucher at www.smartbite.com. Your voucherID is 20001."
    email.sendmail("sengsmartbite@gmail.com", "sengsmartbite@gmail.com", message) 
    email.quit()

def webscrape():
    url = "https://greatist.com/fitness/50-bodyweight-exercises-you-can-do-anywhere#core"
    page = urllib.request.urlopen(url)
    html = page.read().decode("utf-8")
    start_index1 = html.find("<li>Stand with your feet parallel or turned out 15 degrees — whatever is most comfortable.</li>")
    end_index1 = html.find("<li>Make sure your heels do not rise off the floor.</li>")
    squats = html[start_index1:end_index1]
    squats= re.sub("<(li|/li|/ol|ol)>", "", squats)
    squats = squats.replace(".", ". ")

    start_index2 = html.find("<li>Find a step or bench.</li>")
    end_index2 = html.find("<li>Repeat, aiming for 10—12 reps on each side.</li>")
    cardio = html[start_index2:end_index2]
    cardio= re.sub("<(li|/li|/ol|ol)>", "", cardio)
    cardio = cardio.replace(".", ". ")
    return squats, cardio

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
        lastname = (data['ln'].replace('\xa0', '')).strip()
        email = (data['e'].replace('\xa0', '')).strip()
        password = (data['p'].replace('\xa0', '')).strip()
        print(firstname)
        print(lastname)
        print(email)
        print(password)
        #call this function
        seng_db.newuser(firstname, lastname, email, password)
        return
    else:
        return render_template('sign-up.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        jsdata = request.form['javascript_data']
        data = json.loads(jsdata)
        #should print in server terminal
        age = (data['age'].replace('\xa0', '')).strip()
        height = (data['height'].replace('\xa0', '')).strip()
        gender = (data['gender'].replace('\xa0', '')).strip()
        currentweight = (data['cw'].replace('\xa0', '')).strip()
        goalweight = (data['gw'].replace('\xa0', '')).strip()
        print(age)
        print(height)
        print(gender)
        print(currentweight)
        print(goalweight)
        #call this function
        seng_db.registeruser(seng_db.activeUserid, int(age), int(height), gender, int(currentweight), int(goalweight))
        return
    else:
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

@app.route('/welcome')
def success():
    return render_template('success.html')

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

@app.route('/homepage', methods=['POST', 'GET'])
def homepage():
     if request.method == "POST":
        jsdata = request.form['javascript_data']
        data = json.loads(jsdata)
        #should print in server terminal
        if "w" in data:
            weight = (data['w'].replace('\xa0', '')).strip()
            print(weight)
            seng_db.addweight(int(weight))
        if "cal" in data:
            calories = (data['cal'].replace('\xa0', '')).strip()
            print(calories)
            #add cals to db
        if "wat" in data:
            water = (data['wat'].replace('\xa0', '')).strip()
            print(water)
            seng_db.addwater(seng_db.activeUserid, int(water))
        return ""
     else:
        currentweight=seng_db.getcurrentweight(seng_db.activeUserid)
        goalwei=seng_db.getgoalweight(seng_db.activeUserid)
        weileft=seng_db.getweightleft(seng_db.activeUserid)
        watleft=seng_db.getwater(seng_db.activeUserid)
        percentweight=seng_db.weightprog(seng_db.activeUserid)
        percentwater=seng_db.waterprog(seng_db.activeUserid)
        return render_template('home-page.html', currweight = currentweight, goalweight = goalwei, weightleft = weileft, waterleft = watleft, weightpercent = percentweight, waterpercent = percentwater )

@app.route('/createpost')
def createpost():
    return render_template('createpost.html')

@app.route('/personaltrainer')
def personaltrainer():
    return render_template('personal-trainer.html')

@app.route('/foodsearch')
def foodsearch():
    return render_template('foodsearch.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/recommendedexcercise')
def recommendedex():
    return render_template('recommended-exercise.html', webscrapedata = webscrape())

@app.route('/recommenderecipes')
def recommendedrec():
    return render_template('recommended-recipes.html')

@app.route('/rewards', methods=['POST', 'GET'])
def rewards():
    if request.method == "POST":
        sendemail()
    else:
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
