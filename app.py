from flask import Flask, render_template, request, redirect, url_for, session, flash
from data import secret
import sqlite3  # enable control of an sqlite database
app = Flask(__name__)

username = ""
password = ""
app.secret_key = secret.main()
waitlist= []
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
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
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
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\""  # check if username is already in database
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp:  # if username is in database...
        return "Username already exists. Please give another username."
    else:
        return "done"  # if username is not in database


def check_pwd(user, pwd):  # function for checking if a password is correct
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\""  # check if password is in database for the username
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp:  # if password is in database...
        return "done"
    else:
        return "Old password is incorrect."  # if username is not in database

def edit_name(old_user, new_user):  # function for editing the username
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove()
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "UPDATE users SET username = \"" + new_user + "\" WHERE username = \"" + old_user + "\";"  # update username
    c.execute(command)
    db.commit()
    db.close()
    return "done"


def edit_pwd(old_pwd, new_pwd):  # function for changing password
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove()
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "UPDATE users SET password = \"" + new_pwd + "\" WHERE password = \"" + old_pwd + "\""  # update password
    c.execute(command)
    db.commit()
    db.close()
    return "done"  # if username is not in database


# =================== Part 2: Routes ===================

@app.route("/")  # landing page
def start():
    print(app)
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if 'user' in session:  # keeps user logged in
        return redirect(url_for("story"))
    else:  # for new users
        return render_template('landing.html')


@app.route("/auth", methods=["GET", "POST"])  # checking user login credentials
def authenticate():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
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
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
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
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
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
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('searchpage.html')


@app.route("/searchresults", methods=["GET", "POST"])  # search results page
def take():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
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
    c.execute(command)
    search_results = c.fetchall() #get the results of the selection
    collection=[]
    for item in search_results:
        if str(item) not in collection:
            collection.append(str(item)) #make tuple into strings
    db.commit()  # save changes
    db.close()  # close database
    return render_template('searchresults.html', key=request.form['keywords'],
                                                 tagged=request.form['tags'],
                                                 results=collection)

@app.route("/allstories")
def displayAll():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command="SELECT story_title from edits"
    c.execute(command)
    all=c.fetchall()
    count = 0
    collection=[]
    for item in all:
        if str(item) not in collection:
            collection.append(str(item)[2:-3])
    sorted(collection)
    db.commit()  # save changes
    db.close()
    return render_template('allstory.html', display=collection)

@app.route("/logout")  # log out
def logout():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only allow logout if there is a user session running
        return redirect(url_for("start"))
    session.pop('user')  # remove user from session
    flash("You have successfully logged out.")
    return render_template('landing.html')  # redirects to login page


@app.route("/addstory")  # new story page
def plus_story():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    return render_template('storycreator.html')


@app.route("/story", methods=["GET", "POST"])  # submission page of new story input
def see_entry():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
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
    if len(waitlist)==0 and ip not in waitlist:
        waitlist.append(request.environ["REMOTE_ADDR"])
    if waitlist[0]!=ip:
        return "Please refresh after "+str(waitlist.index(p))+" minutes as someone is currently editing."
    #another "if"?
    else:
        db = sqlite3.connect(DB_FILE)
        command = "SELECT story FROM edits"
        c.execute(command)
        all_edits = c.fetchall()
        all_edits = str(all_edits[0])[2:-3]
        all_edits_list = all_edits.split("|")
        previous = all_edits_list[-1]
        return render_template("storyeditor.html", previous_edit = previous)
#def retrieve_latest():  # only go to this page if there's a user
#    if session.get('user') is None:
#        return redirect(url_for("start"))
#    return "Under construction."


@app.route("/viewstory")  # read full story
def view():  # only go to this page if there's a user
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    waitlist.remove(ip)
    if session.get('user') is None:
        return redirect(url_for("start"))
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        new_entry = request.form['new_entry']
        if new_entry == "":
            flash("Please enter something for the new entry.")
            return redirect(url_for("queue")) #no entry, goes back to editing story
        else:
            #Updates Database
            #commands and stuff
            return render_template("viewstory.html", title = title, entire_story = entire_story)


@app.route("/updateprofile")
def update():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove()
    if session.get('user') is None:  # only go to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('editprofile.html')


@app.route("/updateprofilecheck", methods=["GET", "POST"])
def update_check():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove()
    old_username = request.form['old_username'] # retrieve html form information
    old_password = request.form['old_password']
    username = request.form['new_username']
    password = request.form['new_password']
    password_again = request.form['passwordagain']
    print(session['user'])   # if user wants to change username
    if (request.form.get('change_user')):
        if (username != None and old_username == "") or (username == "" and old_username != None):  #check if both fields are inputted
            flash("Please fill in both your old and new username to update your profile.")
            return render_template('editprofile.html')
        if (username == old_username):
            flash("Your old and new username are the same. Nothing will be changed.")
            return render_template('editprofile.html')
        if check_sign(old_username) != "done":  # if the old username is correct...
            check = check_sign(username)  # check if new username is valid
            if check != "done":   # if it isn't valid, flash error message
                flash("" + check)
                return render_template('editprofile.html')
            else:  #otherwise, change username
                print(edit_name(old_username, username))
                session['user'] = username  # change session name
                if not(request.form.get('change_pwd')):
                    flash("Your username has been updated.")
                    return render_template('editprofile.html')
        else:
            flash("Old username is incorrect.")
            return render_template('editprofile.html')
    if(request.form.get('change_pwd')):   # if user wants to change username
        if (password != None and old_password == "") or (password == "" and old_password != None):  #check if both fields are inputted
            flash("Please fill in both your old and new information to update your profile.")
            return render_template('editprofile.html')
        if (password == old_password):
            flash("Your old and new password are the same. Nothing will be changed.")
            return render_template('editprofile.html')
        if password != password_again:
            flash("Password does not match.")
            return render_template('editprofile.html')
        check = check_pwd(session['user'], password)  # check if old password is correct
        if(check != "done"):
            flash("" + check)
            return render_template('editprofile.html')
        else:
            edit_pwd(old_password, password)  # change password
            flash("Login with the new password.")  # go back to login
            return render_template('landing.html')
    else:
        return render_template('editprofile.html')




if __name__ == "__main__":
    app.debug = True
    app.run()
