import sqlite3,sys

#create database
conn = sqlite3.connect('smartbite.db')
cur = conn.cursor()

#create tables
create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                    userid integer PRIMARY KEY,
                                    username text NOT NULL,
                                    password text NOT NULL,
                                    email text NOT NULL,
                                    firstname text,
                                    lastname text,
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

#enter in a new user
action = """INSERT INTO user (userid, username, password, email)
VALUES (0, 'user1', 'password', 'email@gmail.com');"""
cur.execute(action)

#now check if data is entered
action = "SELECT user.userid, user.username, user.password from user;"
cur.execute(action)

#prints the tuples
print(cur.fetchall())

#enter in other user details
action = """UPDATE user
SET firstname = 'John', lastname = 'smith', age = 20
WHERE userid = 0;
"""
cur.execute(action)

action = "SELECT * from user;"
cur.execute(action)

#prints the tuples
print(cur.fetchall())