import sqlite3,sys,os

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
                                        likes text,
                                        dislikes text
                                    );"""

    create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                                        commentid integer PRIMARY KEY,
                                        authorid integer,
                                        content text,
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

if __name__== "__main__":
    main()
    newuser('John', 'Smith', 'email', 'password')
    newuser('Emily', 'Jane', 'email', 'password')
    registeruser(1, 20, 153, 'Female', 50, 70)
    os.remove("smartbite.db")