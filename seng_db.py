import sqlite3,sys,os
from datetime import datetime

activeUserid = None

def main():
    #create database
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #create tables
    create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        userid integer PRIMARY KEY,
                                        firstname text NOT NULL,
                                        lastname text NOT NULL,
                                        email text NOT NULL,
                                        password text NOT NULL,
                                        age integer,
                                        height integer,
                                        goalweight integer,
                                        currentweight integer,
                                        gender text,
                                        points integer,
                                        followerslist text,
                                        followinglist text,
                                        postslist text
                                    );"""

    create_consumption_table = """CREATE TABLE IF NOT EXISTS consumption (
                                        consumptionid integer PRIMARY KEY,
                                        day text,
                                        caloriegoal integer,
                                        calorieconsumed integer,
                                        watergoal integer,
                                        waterconsumed integer,
                                        user_id integer,
                                        FOREIGN KEY (user_id) REFERENCES user (userid)
                                    );"""

    create_fooddiary_table = """CREATE TABLE IF NOT EXISTS fooddiary (
                                        fooddiaryid integer PRIMARY KEY,
                                        timestamp text,
                                        itemslist text,
                                        user_id integer,
                                        FOREIGN KEY (user_id) REFERENCES user (userid)
                                    );"""

    create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                        postid integer PRIMARY KEY,
                                        authorid integer,
                                        title text,
                                        content text,
                                        time text,
                                        likes text,
                                        dislikes text
                                    );"""

    create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                                        commentid integer PRIMARY KEY,
                                        authorid integer,
                                        content text,
                                        time text,
                                        post_id integer,
                                        FOREIGN KEY (post_id) REFERENCES posts (postid)
                                    );"""

    #now create all the tables
    cur.execute(create_user_table)
    cur.execute(create_consumption_table)
    cur.execute(create_fooddiary_table)
    cur.execute(create_posts_table)
    cur.execute(create_comments_table)

    conn.close()

#add new user details
def newuser(firstname, lastname, email, password):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #generate user id
    action = "SELECT MAX(userid) from user"
    cur.execute(action)
    data = cur.fetchall()

    ##if there are no values
    if (data[0][0] == None):
        userid = 0
    else:
        userid = data[0][0] + 1

    #set the active user id
    global activeUserid
    activeUserid = userid

    #enter in a new user
    action = "INSERT INTO user (userid, firstname, lastname, email, password) VALUES (?, ?, ?, ?, ?)"
    cur.execute(action, (userid, firstname, lastname, email, password))

    #generate timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y")

    action = "SELECT * from consumption where day = {} and user_id = {}".format(timestamp_string, userid)
    cur.execute(action)
    data = cur.fetchall()

    if not data:
        #generate consumption id
        action = "SELECT MAX(consumptionid) from consumption"
        cur.execute(action)
        data = cur.fetchall()

        ##if there are no values
        if (data[0][0] == None):
            consumptionid = 0
        else:
            consumptionid = data[0][0] + 1

        #enter in a new consumption id and date
        action = "INSERT INTO consumption (consumptionid, day, caloriegoal, calorieconsumed, watergoal, waterconsumed, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(action, (consumptionid, timestamp_string, 2500, 0, 8, 0, userid))

    #now check if data is entered
    action = "SELECT user.userid, user.firstname, user.lastname from user;"
    cur.execute(action)
    conn.commit()

    #prints the tuples
    print(cur.fetchall())

    conn.close()

#register user
def registeruser(userid, age, height, gender, currentweight, goalweight):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #enter in other user details
    action = "UPDATE user SET age = ?, height = ?, gender = ?, currentweight = ?, goalweight = ? where userid = ?"
    cur.execute(action, (age, height, gender, currentweight, goalweight, userid))

    action = "SELECT * from user;"
    cur.execute(action)

    #prints the tuples
    print(cur.fetchall())
    conn.commit()
    conn.close()

#login user
def login(email, password):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #get the matching password of the email
    action = "SELECT user.email from user where user.email='{}'".format(email)
    cur.execute(action)

    #if email does not exist
    if not cur.fetchall():
        print(email)
        return 'Email does not exist'

    #get the matching password of the email
    action = "SELECT user.password, user.userid from user where user.email='{}'".format(email)
    cur.execute(action)
    data = cur.fetchall()

    #check if passwords match
    if (data[0][0] == password):
        global activeUserid
        activeUserid = data[0][1]
        #check if the consumption table for this day and user exists
        #generate timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y")

    action = "SELECT * from consumption where day = {} and user_id = {}".format(timestamp_string, activeUserid)
    cur.execute(action)
    data = cur.fetchall()

    if not data:
        #generate consumption id
        action = "SELECT MAX(consumptionid) from consumption"
        cur.execute(action)
        data = cur.fetchall()

        ##if there are no values
        if (data[0][0] == None):
            consumptionid = 0
        else:
            consumptionid = data[0][0] + 1

        #enter in a new consumption id and date
        action = "INSERT INTO consumption (consumptionid, day, caloriegoal, calorieconsumed, watergoal, waterconsumed, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(action, (consumptionid, timestamp_string, 2500, 0, 8, 0, activeUserid))
        return 'Login successful'
    else:
        return 'Incorrect password'
    conn.close()

#given a userid, get the weight left
def getweightleft(userid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #get the currentweight, goalweight
    action = "SELECT user.currentweight, user.goalweight from user where user.userid = {}".format(userid)
    cur.execute(action)
    data = cur.fetchall()

    currentweight = data[0][0]
    goalweight = data[0][1]
    conn.close()

    return abs(currentweight - goalweight)

def addwater(userid, glasses):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #generate timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y")

    #enter in other user details
    action = "UPDATE consumption SET waterconsumed ={} where user_id = {} and day = '{}'".format(glasses, userid, timestamp_string)
    cur.execute(action)

    action = "SELECT * from consumption;"
    cur.execute(action)

    #prints the tuples
    print(cur.fetchall())
    conn.commit()
    conn.close()

#given a userid, get water left
def getwater(userid):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #get the currentweight, goalweight
    action = "SELECT watergoal, waterconsumed from consumption where user_id = {}".format(userid)
    cur.execute(action)
    data = cur.fetchall()

    watergoal = data[0][0]
    waterconsumed = data[0][1]
    conn.close()

    if waterconsumed > 8:
        return 0
    else:
        return (watergoal - waterconsumed)

def addcalories(userid, calories):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #generate timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y")

    #enter in other user details
    action = "UPDATE consumption SET calorieconsumed ={} where user_id = {} and day = '{}'".format(calories, userid, timestamp_string)
    cur.execute(action)
    conn.commit()
    action = "SELECT * from consumption;"
    cur.execute(action)

    #prints the tuples
    print(cur.fetchall())
    conn.close()

def getcalories(userid):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #get the currentweight, goalweight
    action = "SELECT caloriegoal, calorieconsumed from consumption where consumption.user_id = {}".format(userid)
    cur.execute(action)
    data = cur.fetchall()
    caloriegoal = data[0][0]
    calorieconsumed = data[0][1]
    conn.close()

    if calorieconsumed > 2500:
        return 0
    else:
        return (caloriegoal - calorieconsumed)

#def editprofile():

def create_post(title, content, authorid):

    #generate postid
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #generate user id
    action = "SELECT MAX(postid) from posts"
    cur.execute(action)
    data = cur.fetchall()

    ##if there are no values
    if (data[0][0] == None):
        postid = 0
    else:
        postid = data[0][0] + 1

    #generate timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y %H:%M")

    #enter in a new post
    action = "INSERT INTO posts (postid, authorid, title, content, time) VALUES (?, ?, ?, ?, ?)"
    cur.execute(action, (postid, authorid, title, content, timestamp_string))

    #print 
    action = "SELECT * from posts where posts.authorid='{}'".format(authorid)
    cur.execute(action)
    print(cur.fetchall())

    conn.commit()
    conn.close()

def edit_post(postid, newcontent, authorid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #check if the given id is same as author
    action = "SELECT posts.authorid from posts where posts.postid={}".format(postid)
    cur.execute(action)

    postauthor = cur.fetchall()[0][0]
    if (postauthor != authorid):
        print("You cannot edit post")

    #generate new timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y %H:%M")

    #update timestamp
    action = "UPDATE posts SET content ='{}', time ='{}' where authorid = {}".format(newcontent, timestamp_string, authorid)
    cur.execute(action)

    #print
    action = "SELECT * from posts where posts.authorid='{}'".format(authorid)
    cur.execute(action)
    print(cur.fetchall())

    conn.commit()
    conn.close()


def createcomment(authorid, content, postid):

    #generate new commentid
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #generate user id
    action = "SELECT MAX(commentid) from comments"
    cur.execute(action)
    data = cur.fetchall()

    ##if there are no values
    if (data[0][0] == None):
        commentid = 0
    else:
        commentid = data[0][0] + 1

    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y %H:%M")

    #insert into comments table
    action = "INSERT INTO comments (commentid, authorid, content, time, post_id) VALUES (?, ?, ?, ?, ?)"
    cur.execute(action, (commentid, authorid, content, timestamp_string, postid))

    action = "SELECT * from comments;"
    cur.execute(action)

    #prints the tuples
    print(cur.fetchall())
    conn.commit()
    conn.close()

def editcomment(authorid, newcomment, commentid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #check if the given id is same as author
    action = "SELECT authorid from comments where commentid={}".format(commentid)
    cur.execute(action)

    commentauthor = cur.fetchall()[0][0]
    if (commentauthor != authorid):
        print("You cannot edit post")

    #generate new timestamp
    now = datetime.now()
    timestamp_string = now.strftime("%d/%m/%Y %H:%M")

    #update timestamp
    action = "UPDATE comments SET content ='{}', time ='{}' where authorid = {}".format(newcomment, timestamp_string, authorid)
    cur.execute(action)

    #print
    action = "SELECT * from comments"
    cur.execute(action)
    print(cur.fetchall())

    conn.commit()
    conn.close()

def deletecomment(authorid, commentid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #check if the given id is same as author
    action = "SELECT authorid from comments where commentid={}".format(commentid)
    cur.execute(action)

    commentauthor = cur.fetchall()[0][0]
    if (commentauthor != authorid):
        print("You cannot delete post")

    #update timestamp
    action = "DELETE from comments where commentid = {}".format(commentid)
    cur.execute(action)

    #print
    action = "SELECT * from comments"
    cur.execute(action)
    print(cur.fetchall())

    conn.commit()
    conn.close()

def settings_updateemail(newemail, userid):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #enter in other user details
    action = "UPDATE user SET email ='{}' where userid = {}".format(newemail, userid)
    cur.execute(action)

    action = "SELECT * from user;"
    cur.execute(action)

    #prints the tuples
    print(cur.fetchall())
    conn.commit()
    conn.close()

def settings_updatepassword(newpassword, userid):
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #enter in other user details
    action = "UPDATE user SET password ='{}' where userid = {}".format(newpassword, userid)
    cur.execute(action)

    action = "SELECT * from user;"
    cur.execute(action)

    #prints the tuples
    print(cur.fetchall())
    conn.commit()
    conn.close()

def logout(userid):
    global activeUserid
    activeUserid = None

if __name__== "__main__":
    main()
    #newuser('John', 'Smith', 'john@email.com', 'password')
    newuser('Emily', 'Jane', 'emily@email.com', 'password')
    registeruser(0, 20, 153, 'Female', 50, 70)
    #settings_updateemail('emilyjane@email.com', 1)
    #settings_updateemail('newpassword', 1)
    #print(login('john@email.com', 'password'))
    #addcalories(0, 1200)
    #addwater(0, 5)
    #print(getcalories(1))
    create_post('hello', 'hello', 0)
    createcomment(0, "nice", 0)
    createcomment(0, "WOW", 0)
    deletecomment(0, 0)
    #editcomment(0, "hello", 0)
    #edit_post(0, "bye", 0)
    #print(getweightleft(1))
    #print(getwater(0))
    #print(getcalories(0))
    os.remove("smartbite.db")