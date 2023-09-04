from flask import Flask
from flask import request, make_response, redirect
from markupsafe import escape

import sqlite3


app = Flask(__name__)


@app.route("/products")
def products():
    con = sqlite3.connect("fordCache.db")
    cur = con.cursor()
    sql = f"SELECT id,name,desc,cost FROM products"
    res = cur.execute(sql)
    products = res.fetchall()
    if (products == None):
        return make_response("User not found", 404)
    else:
        res = []
        for product in products:
            productJSON = {
                "id": product[0],
                "name": product[1],
                "desc": product[2],
                "cost": product[3]
            }
            res.append(productJSON)
        return res


@app.route("/login", methods=['POST'])
def login():
    con = sqlite3.connect("fordCache.db")

    cur = con.cursor()

    usernameInp = request.json["username"]
    passwordInp = request.json["password"]
    sql = f"SELECT id,username,email,points,profileImage FROM users WHERE username='{str(escape(usernameInp))}' and password='{str(escape(passwordInp))}'"
    res = cur.execute(sql)
    user = res.fetchone()
    if (user == None):
        return make_response("User not found", 404)
    else:
        userJson = {
            "userId": user[0],
            "username": user[1],
            "email": user[2],
            "points": user[3],
            "profilePicture": user[4]
        }
        return userJson


@app.route("/signup", methods=['POST'])
def signup():

    con = sqlite3.connect("fordCache.db")
    cur = con.cursor()

    usernameInp = request.json["username"]
    emailInp = request.json["username"]
    passwordInp = request.json["password"]

    sql = f"INSERT INTO users (username, password, email,points, profileImage) VALUES ('{usernameInp}', '{passwordInp}', '{emailInp}',  10000,  'assets/images/default_user.png');"

    res = cur.execute(sql)
    con.commit()

    sql = f"SELECT id,username,email,points,profileImage FROM users WHERE username='{str(escape(usernameInp))}' and password='{str(escape(passwordInp))}'"
    res = cur.execute(sql)
    user = res.fetchone()
    if (user == None):

        return make_response("User not found", 404)
    else:
        userJson = {
            "userId": user[0],
            "username": user[1],
            "email": user[2],
            "points": user[3],
            "profilePicture": user[4]
        }
        return userJson
