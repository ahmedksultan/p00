from flask import Flask, render_template, request, redirect, url_for, session, flash
from data import secret
import sqlite3  # enable control of an sqlite database
app = Flask(__name__)

username = ""
password = ""
app.secret_key = secret.main()
waitlist= []
editing=False;
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
        db = sqlite3.connect(DB_FILE)  # open database
        c = db.cursor()
        command="SELECT stories_edited FROM users WHERE \""+session.get('user')+"\" =username"
        c.execute(command)
        mystories = c.fetchall() #get the results of the selection
        mystories=str(mystories[0])[2:-3]
        collection=mystories.split(",")
        db.commit()  # save changes
        db.close()  # close database
        return render_template('homepage.html', name=session['user'], storycoll=collection)


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
    if keywords == "" and tags == "": #refresh page is no input but submitted
        return render_template('searchpage.html')
    if len(tags) > 0: #if tag is inputted, split tag to seperate tags
        tags = tags.strip().split(" ")
    if len(keywords) > 0: #if key words typed in, split keywords into seperate tags
        keywords = keywords.strip().split(" ")
        command = "SELECT story_title FROM edits WHERE " #begin selecting story titles that match keywords
        count = 0
        while count < len(keywords): #loop through to see if any titles contain the keywords inputted
            if count == len(keywords)-1:
                command += "story_title LIKE \"%" + keywords[count] + "%\" "
            else:
                command += "story_title LIKE \"%" + keywords[count] + "%\" OR "
            count += 1
    if len(tags) > 0 and len(keywords) == 0: #if only tags tinputed
        command = "SELECT story_title FROM edits WHERE " #begin selecting story titles that match tags
        count = 0
        while count < len(tags): #loop through to see if any stories contain the tags inputted
            if count == len(tags) - 1:
                command += "tags LIKE \"%" + tags[count] + "%\" "
            else:
                command += "tags LIKE \"%" + tags[count] + "%\" OR "
            count += 1
    if len(keywords) > 0 and len(tags) > 0: #if both search fields are inputted
        count = 0
        while count < len(tags): #loop through tags because keywords are already searched
            command += " OR tags LIKE \"%"+tags[count]+"%\" " #loop through to find stories that containted those tags
            count += 1
    command += ";"
    print(command)
    c.execute(command)
    search_results = c.fetchall() #get the results of the selection
    collection=[]
    for item in search_results:
        collection.append(str(item)) #make tuple into strings
    db.commit()  # save changes
    db.close()  # close database
    return render_template('searchresults.html', key=request.form['keywords'],
                                                 tagged=request.form['tags'],
                                                 results=collection)

@app.route("/allstories")
def displayAll():
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command="SELECT story_title from edits"
    c.execute(command)
    all=c.fetchall()
    count = 0
    collection=[]
    for item in all:
        collection.append(str(item)[2:-3])
    db.commit()  # save changes
    db.close()
    return render_template('allstory.html', display=collection)

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
def queue():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if(len(waitlist)==0 and ip not in waitlist):
        editing=True;
        waitlist.append(request.environ["REMOTE_ADDR"])
    return str(len(waitlist))
#def retrieve_latest():  # only go to this page if there's a user
#    if session.get('user') is None:
#        return redirect(url_for("start"))
#    return "Under construction."


@app.route("/viewstory")  # read full story
def view():  # only go to this page if there's a user
    if session.get('user') is None:
        return redirect(url_for("start"))
    return "Under construction."


if __name__ == "__main__":
    app.debug = True
    app.run()
