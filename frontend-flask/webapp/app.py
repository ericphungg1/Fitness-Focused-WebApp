from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/signup')
def signup():
    return render_template('sign-up.html')

@app.route('/register')
def register():
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
    return render_template('recommended-exercise.html')

@app.route('/recommenderecipes')
def recommendedrec():
    return render_template('recommended-recipes.html')

@app.route('/rewards')
def rewards():
    return render_template('rewards.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
