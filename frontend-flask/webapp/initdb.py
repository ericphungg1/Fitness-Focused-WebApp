import sqlite3,sys,os

def init():

    if os.path.isfile('smartbite.db'):
        os.remove('smartbite.db')

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

