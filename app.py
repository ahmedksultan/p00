
from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)

username = ""
password = ""
app.secret_key = "abcd"

import sqlite3   #enable control of an sqlite database

DB_FILE= "foldoverdata.db"


#function for adding a user into the users database
def adduser(username, password, admin):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops
    command = "INSERT INTO users (username, password, is_admin) VALUES (\"" + username + "\", \"" + password + "\", " + str(admin) + ")"
    c.execute(command)
    db.commit()
    db.close()
    return "done"

#function for checking if a user's login credentials are correct
def checkuser(user, pwd):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops
    command = "SELECT password FROM users WHERE username = \"" + user + "\""
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp != None:
        checkpass = temp[0]
        if checkpass == pwd:
            return "done"
        else: return "Password is incorrect."
    else:
        return "Username does not exist."

#landing page
@app.route("/")

def start():
    print(app)
    if 'user' in session: #keeps user logged in
          return redirect (url_for("story"))
    else: #for new user
        flash("Please log in.")
        return render_template('landing.html')

@app.route("/auth")

def authenticate():
    username = request.args['username']
    password = request.args['password']
    check = checkuser(username, password)
    if(check == "done"):
        session['user'] = username
        return redirect (url_for("story"))
    else:
        flash("" + check)
        return render_template('landing.html')

@app.route("/signup")

def sign():
    return render_template('signup.html')

@app.route("/signupcheck")

def signcheck():
    username = request.args['username']
    password = request.args['password']
    passwordagain = request.args['passwordagain']
    if passwordagain == password:
        if(adduser(username, password, 0) == "done"):
            session['user'] = request.args['username']
            return redirect (url_for("story"))
        else: return "No"
    else:
        flash("Password does not match.")
        return render_template('signup.html')


@app.route("/mystories")

def story():
    return render_template('homepage.html')

@app.route("/search")

def find():
    return "Hello"

@app.route("/logout")

def logout():
    session.pop('user')
    flash("You have successfully logged out.")
    return render_template('landing.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

# db.commit() #save changes
# db.close()  #close database
