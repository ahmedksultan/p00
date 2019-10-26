
from flask import Flask, render_template, request, redirect, url_for, session, flash
from data import secret
import sqlite3  # enable control of an sqlite database
app = Flask(__name__)

username = ""
password = ""
app.secret_key = secret.main()

DB_FILE = "foldoverdata.db"

# =================== Part 1: Database Accessing Functions ==============


def add_user(user, passphrase, admin):  # function for adding a user into the users database
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "INSERT INTO users (username, password, is_admin) " \
              "VALUES (\"" + user + "\", \"" + passphrase + "\", " + str(admin) + ")"
    c.execute(command)  # store a new user's name and password
    db.commit()
    db.close()
    return "done"


def check_user(user, pwd):  # function for checking if a user's login credentials are correct
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\""  # check if username is in database
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp:  # if username is in database...
        checkpass = temp[0]  # check if password is correct
        if checkpass == pwd:
            return "done"
        else:
            return "Password is incorrect."
    else:
        return "Username does not exist."  # if username is not in database


def check_sign(user):  # function for checking if a new user's username already exists in database
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\""  # check if username is already in database
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp:  # if username is in database...
        return "Username already exists. Please give another username."
    else:
        return "done"  # if username is not in database


# =================== Part 2: Routes ==============

@app.route("/")
def start():  # landing page
    print(app)
    if 'user' in session:  # keeps user logged in
        return redirect(url_for("story"))
    else:  # for new user
        flash("Please log in.")
        return render_template('landing.html')


@app.route("/auth")
def authenticate():  # checking user login credentials
    username = request.args['username']  # retrieve html form username and password
    password = request.args['password']
    if username == "":  # if there is no input
        flash("Please enter a username.")
        return render_template('landing.html')
    check = check_user(username, password)  # check database for username and password
    if check == "done":
        session['user'] = username
        return redirect(url_for("story"))  # redirect to homepage if credentials are correct
    else:  # otherwise flash error message
        flash("" + check)
        return render_template('landing.html')


@app.route("/signup")
def sign():  # go to sign up page
    return render_template('signup.html')


@app.route("/signupcheck")  # check sign up information
def signcheck():
    username = request.args['username']  # retrieve html form username and password
    password = request.args['password']
    password_again = request.args['passwordagain']
    if username == "":  # if there is no input
        flash("Please give a username.")
        return render_template('signup.html')
    else:
        check = check_sign(username)  # check if username already exists in database
        if check != "done":
            flash("" + check)
            return render_template('signup.html')
    if password == "":  # check if password input is empty
        flash("Please give a username and password.")
        return render_template('signup.html')
    if password_again == password:  # check to make sure both passwords are the same
        if add_user(username, password, 0) == "done":
            session['user'] = request.args['username']
            return redirect(url_for("story"))  # if everything is correct, sign up and redirect to homepage
    else:  # otherwise flash error message
        flash("Password does not match.")
        return render_template('signup.html')


@app.route("/mystories")
def story():  # homepage
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('homepage.html')


@app.route("/search")
def find():  # search page
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('searchpage.html')


@app.route("/searchresults")
def take():
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect (url_for("start"))
    keywords = request.args['keywords']  # retrieve search input
    tags = request.args['tags']
    if keywords == "" and tags == "":
        return render_template('searchpage.html')
    return "done"


@app.route("/logout")
def logout():
    if session.get('user') is None:  # only allow logout if there is a user session running
        return redirect(url_for("start"))
    session.pop('user')  # remove user from session
    flash("You have successfully logged out.")
    return render_template('landing.html')


@app.route("/story")
def read_story():
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    return render_template('newstory.html')


@app.route("/editstory")
def retrieve_latest():  # only go to this page if there's a user
    if session.get('user') is None:
        return redirect(url_for("start"))
    return "get latest edit here"


if __name__ == "__main__":
    app.debug = True
    app.run()
