
from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)

username = "Eggs"
password = "friedrice"
app.secret_key = "abcd"

import sqlite3   #enable control of an sqlite database

DB_FILE= "foldoverdata.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#command = "CREATE TABLE users (username TEXT, password TEXT, stories_edited BLOB, is_admin INTEGER)"
#c.execute(command)

@app.route("/")

def start():
    print(app)
    if 'user' in session: #keeps user logged in
         return redirect (url_for("homepage"))
    else: #for new user
        flash("Please log in.")
        return render_template('landing.html')

@app.route("/auth")

def authenticate():
    session['user'] = request.args['username']
    session['password'] = request.args['password']
    return redirect (url_for("story"))

@app.route("/signup")

def sign():
    return render_template('signup.html')

@app.route("/signupcheck")

def signcheck():
    command = "INSERT INTO users VALUES (\"" + request.args['username'] + "\", \"" + request.args['password'] + "\", "" , 1)"
    c.execute(command)

@app.route("/mystories")

def story():
    return render_template('homepage.html')

@app.route("/search")

def find():
    return "Hello"

# @app.route("/auth")
# def authenticate(): #checks to match user and pass
#     session['user'] = request.args['username']
#     print(session['user'])
#     if (request.args['username'] == username and request.args['password'] == password) :
#        return redirect (url_for("welcome")) #goes to welcome page if credentials are correct
#     else:
#        return redirect (url_for("err")) #goes to error page is wrong

if __name__ == "__main__":
    app.debug = True
    app.run()

db.commit() #save changes
db.close()  #close database
