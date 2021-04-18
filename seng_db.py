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
                                        clorieconsumed integer,
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
        return 'Login successful'
    else:
        return 'Incorrect password'
    conn.close()

def view_posts():

    #generate postid
    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #print 
    action = "SELECT * from posts"
    cur.execute(action)
    print(cur.fetchall())

    conn.commit()
    conn.close()

def delete_posts(post_id, authorid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #check if the given id is same as author
    action = "SELECT posts.authorid from posts where posts.postid={}".format(postid)
    cur.execute(action)

    postauthor = cur.fetchall()[0][0]
    if (postauthor != authorid):
        print("You cannot delete this post")

    action = "DELETE * from posts where posts.postid='{}'".format(postid)
    action = "DELETE * from comments where comments.postid='{}'".format(postid)

    cur.execute(action)
    conn.commit()
    conn.close()

def like_post(postid, userid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #check if the given id is same as author
    action = "SELECT posts.likes from posts where posts.postid={}".format(postid)
    cur.execute(action)

    likes = cur.fetchall()[0][0]
    on = 1
    off = 0
    if (likes != 1):
        action = "UPDATE posts SET like = '{}'".format(on)
        cur.execute(action)
        # Do you need to SELECT the dislike attribute before updating?
        action = "UPDATE posts SET dislike = '{}'".format(off) 
        cur.execute(action)

    conn.commit()
    conn.close()

def dislike_post(postid, userid):

    conn = sqlite3.connect('smartbite.db')
    cur = conn.cursor()

    #check if the given id is same as author
    action = "SELECT posts.dislikes from posts where posts.postid={}".format(postid)
    cur.execute(action)

    likes = cur.fetchall()[0][0]
    on = 1
    off = 0
    if (likes != 1):
        action = "UPDATE posts SET dislike = '{}'".format(on)
        cur.execute(action)
        # Do you need to SELECT the like attribute before updating?
        action = "UPDATE posts SET like = '{}'".format(off) 
        cur.execute(action)

    conn.commit()
    conn.close()

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
    newuser('John', 'Smith', 'john@email.com', 'password')
    newuser('Emily', 'Jane', 'emily@email.com', 'password')
    registeruser(1, 20, 153, 'Female', 50, 70)
    settings_updateemail('emilyjane@email.com', 1)
    settings_updateemail('newpassword', 1)
    print(login('john@email.com', 'password'))
    create_post('hello', 'hello', 0)
    edit_post(0, "bye", 0)
    os.remove("smartbite.db")