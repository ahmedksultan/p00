
from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)

username = ""
password = ""
app.secret_key = "abcd"

import sqlite3   #enable control of an sqlite database

DB_FILE= "foldoverdata.db"

#=================== Part 1: Database Accessing Functions ==============

#function for adding a user into the users database
def adduser(username, password, admin):
    db = sqlite3.connect(DB_FILE) #open database
    c = db.cursor()
    command = "INSERT INTO users (username, password, is_admin) VALUES (\"" + username + "\", \"" + password + "\", " + str(admin) + ")"
    c.execute(command) #store a new user's name and password
    db.commit()
    db.close()
    return "done"

#function for checking if a user's login credentials are correct
def checkuser(user, pwd):
    db = sqlite3.connect(DB_FILE) #open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\"" #check if username is in database
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp != None: #if username is in database...
        checkpass = temp[0] #check if password is correct
        if checkpass == pwd:
            return "done"
        else: return "Password is incorrect."
    else:
        return "Username does not exist." #if username is not in database

#function for checking if a new user's username already exists in database
def checksign(user):
    db = sqlite3.connect(DB_FILE) #open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\"" #check if username is already in database
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp != None: #if username is in database...
        return "Username already exists. Please give another username."
    else: return "done" #if username is not in database



#=================== Part 2: Routes ==============

#landing page
@app.route("/")

def start():
    print(app)
    if 'user' in session: #keeps user logged in
          return redirect (url_for("story"))
    else: #for new user
        flash("Please log in.")
        return render_template('landing.html')

#checking user login credentials
@app.route("/auth")

def authenticate():
    username = request.args['username'] #retrieve html form username and password
    password = request.args['password']
    if username == "": #if there is no input
        flash("Please enter a username.")
        return render_template('landing.html')
    check = checkuser(username, password) #check database for username and password
    if(check == "done"):
        session['user'] = username
        return redirect (url_for("story")) #redirect to homepage if credentials are correct
    else: #otherwise flash error message
        flash("" + check)
        return render_template('landing.html')

#sign up page
@app.route("/signup")

def sign(): #go to sign up page
    return render_template('signup.html')

#check sign up information
@app.route("/signupcheck")

def signcheck():
    username = request.args['username'] #retrieve html form username and password
    password = request.args['password']
    passwordagain = request.args['passwordagain']
    if username == "": #if there is no input
        flash("Please give a username.")
        return render_template('signup.html')
    else:
        check = checksign(username) #check if username already exists in database
        if(check != "done"):
            flash("" + check)
            return render_template('signup.html')
    if password == "": #check if password input is empty
        flash("Please give a username and password.")
        return render_template('signup.html')
    if passwordagain == password: #check to make sure both passwords are the same
        if(adduser(username, password, 0) == "done"):
            session['user'] = request.args['username']
            return redirect (url_for("story")) #if everything is correct, sign up and redirect to homepage
    else: #otherwise flash error message
        flash("Password does not match.")
        return render_template('signup.html')

#homepage
@app.route("/mystories")

def story():
    if session.get('user') is None: #only go to this page if there's a user
        return redirect (url_for("start"))
    else:
        return render_template('homepage.html')

#search page
@app.route("/search")

def find():
    if session.get('user') is None: #only go to this page if there's a user
        return redirect (url_for("start"))
    else:
        return render_template('searchpage.html')

@app.route("/searchresults")

def take():
    if session.get('user') is None: #only go to this page if there's a user
        return redirect (url_for("start"))
    keywords = request.args['keywords'] #retrieve search input
    tags = request.args['tags']
    if keywords == "" and tags == "":
        return render_template('searchpage.html')
    return "done"

#logout
@app.route("/logout")

def logout():
    if session.get('user') is None: #only allow logout if there is a user session running
        return redirect (url_for("start"))
    session.pop('user') #remove user from session
    flash("You have successfully logged out.")
    return render_template('landing.html')

@app.route("/story")

def readStory():
    if session.get('user') is None: #only go to this page if there's a user
        return redirect (url_for("start"))
    return "Don't know how to do this yet."

@app.route("/editstory")

def retrieve_latest(): #only go to this page if there's a user
    if session.get('user') is None:
        return redirect (url_for("start"))
    return "get latest edit here"

if __name__ == "__main__":
    app.debug = True
    app.run()

# db.commit() #save changes
# db.close()  #close database
