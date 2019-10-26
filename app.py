from flask import Flask, render_template, request, redirect, url_for, session, flash
from data import secret
import sqlite3  # enable control of an sqlite database
app = Flask(__name__)

username = ""
password = ""
app.secret_key = secret.main()

DB_FILE = "data/foldoverdata.db"

# =================== Part 1: Database Accessing Functions ===================


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


# =================== Part 2: Routes ===================

@app.route("/")  # landing page
def start():
    print(app)
    if 'user' in session:  # keeps user logged in
        return redirect(url_for("story"))
    else:  # for new users
        return render_template('landing.html')


@app.route("/auth", methods=["GET", "POST"])  # checking user login credentials
def authenticate():
    username = request.form['username']  # retrieve html form username and password
    password = request.form['password']
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


@app.route("/signup")  # go to sign up page
def sign():
    return render_template('signup.html')


@app.route("/signupcheck", methods=["GET", "POST"])  # check sign up information
def signcheck():
    username = request.form['username']  # retrieve html form username and password
    password = request.form['password']
    password_again = request.form['passwordagain']
    if username == "":  # if there is no input for username
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
            session['user'] = request.form['username']
            return redirect(url_for("story"))  # if everything is correct, sign up and redirect to homepage
    else:  # otherwise flash error message
        flash("Password does not match.")
        return render_template('signup.html')


@app.route("/mystories")  # homepage, also lists all the stories edited by user
def story():
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('homepage.html', name=session['user'])


@app.route("/search")  # search page
def find():
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('searchpage.html')


@app.route("/searchresults", methods=["GET", "POST"])  # search results page
def take():
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    keywords = request.form['keywords']  # retrieve search input
    tags = request.form['tags']
    if keywords == "" and tags == "":
        return render_template('searchpage.html')
    if len(tags) > 0:
        tags = tags.strip().split(" ")
    if len(keywords) > 0:
        keywords = keywords.strip().split(" ")
        command = "SELECT story_title FROM edits WHERE "
        count = 0
        while count < len(keywords):
            if count == len(keywords)-1:
                command += "story_title LIKE \"%" + keywords[count] + "%\" "
            else:
                command += "story_title LIKE \"%" + keywords[count] + "%\" OR "
            count += 1
    if len(tags) > 0 and len(keywords) == 0:
        command = "SELECT story_title FROM edits WHERE "
        count = 0
        while count < len(tags):
            if count == len(tags) - 1:
                command += "tags LIKE \"%" + tags[count] + "%\" "
            else:
                command += "tags LIKE \"%" + tags[count] + "%\" OR "
            count += 1
    if len(keywords) > 0 and len(tags) > 0:
        count = 0
        while count < len(tags):
            command += " OR tags LIKE \"%"+tags[count]+"%\" "
            count += 1
    command += ";"
    print(command)
    c.execute(command)
    search_results = c.fetchall()
    collection=[]
    for item in search_results:
        collection.append(str(item))
    db.commit()  # save changes
    db.close()  # close database
    return render_template('searchresults.html', key=request.form['keywords'],
                                                 tagged=request.form['tags'],
                                                 results=collection)


@app.route("/logout")  # log out
def logout():
    if session.get('user') is None:  # only allow logout if there is a user session running
        return redirect(url_for("start"))
    session.pop('user')  # remove user from session
    flash("You have successfully logged out.")
    return render_template('landing.html')  # redirects to login page


@app.route("/addstory")  # new story page
def plus_story():
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    return render_template('storycreator.html')


@app.route("/story", methods=["GET", "POST"])  # submission page of new story input
def see_entry():
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    title = request.form['story_title']  # retrieve story input
    tags = request.form['tags']
    first_entry = request.form['entry_1']
    if title == "" or tags == "" or first_entry == "":  # if there is no input, flash error message and refresh page
        flash("Fill in all the blanks to create a story.")
        return render_template('storycreator.html')
    else:
        return "done"


@app.route("/editstory")  # editing page
def retrieve_latest():  # only go to this page if there's a user
    if session.get('user') is None:
        return redirect(url_for("start"))
    return "Under construction."


@app.route("/viewstory")  # read full story
def view():  # only go to this page if there's a user
    if session.get('user') is None:
        return redirect(url_for("start"))
    return "Under construction."


if __name__ == "__main__":
    app.debug = True
    app.run()