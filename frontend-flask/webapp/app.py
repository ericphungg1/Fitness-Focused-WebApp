from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import initdb
import seng_db
import urllib.request
import re
app = Flask(__name__)

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
    return render_template('calorie_counter.html')

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
    return render_template('recommended-exercise.html', webscrapedata = webscrape())

@app.route('/recommenderecipes')
def recommendedrec():
    return render_template('recommended-recipes.html')

@app.route('/rewards')
def rewards():
    return render_template('rewards.html')

if __name__ == '__main__':
    #initialise database
    initdb.init()
    app.run(debug=True, host='0.0.0.0')
