from flask import Flask, render_template, request, redirect, url_for, session, flash
from data import secret
from datetime import datetime
import sqlite3  # enable control of an sqlite database
app = Flask(__name__)

username = ""
password = ""
app.secret_key = secret.main()
waitlist = []
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
    ip = request.environ["REMOTE_ADDR"]
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
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT password FROM users " \
              "WHERE username = \"" + user + "\""  # check if username is already in database
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp:  # if username is in database...
        return "Username already exists. Please give another username."
    else:
        return "done"  # if username is not in database


def check_pwd(user, pwd):  # function for checking if a password is correct
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT password FROM users WHERE username = \"" + user + "\";"
    # check if password is in database for the username
    cur = c.execute(command)
    temp = cur.fetchone()
    if temp:  # if password is in database...
        checkpass = temp[0]
        if checkpass == pwd:
            return "done"
        else:
            return "Old password is incorrect."
    else:
        return "Old password is incorrect."  # if username is not in database


def edit_name(old_user, new_user):  # function for editing the username
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "UPDATE users SET username = \"" + new_user + "\" " \
                                                            "WHERE username = \"" + old_user + "\";"  # update username
    c.execute(command)
    db.commit()
    db.close()
    return "done"


def edit_pwd(old_pwd, new_pwd):  # function for changing password
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "UPDATE users SET password = \"" + new_pwd + "\" WHERE password = \"" + old_pwd + "\""  # update password
    c.execute(command)
    db.commit()
    db.close()
    return "done"  # if username is not in database


def is_admin():  # check if user is an admin
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT is_admin FROM users WHERE username=" + "\"" + session['user'] + "\";"
    c.execute(command)
    ouptut = int(str(c.fetchall())[2:-3])
    return bool(ouptut)


# =================== Part 2: Routes ===================


@app.route("/")  # landing page
def start():
    # #print(app)
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if 'user' in session:  # keeps user logged in
        return redirect(url_for("story"))
    else:  # for new users
        return render_template('landing.html')


@app.route("/auth", methods=["GET", "POST"])  # checking user login credentials
def authenticate():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
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
    ip = request.environ["REMOTE_ADDR"]
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
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    else:
        db = sqlite3.connect(DB_FILE)  # open database
        c = db.cursor()
        command = "SELECT stories_edited FROM users WHERE \""+session.get('user')+"\" =username;"
        c.execute(command)
        mystories =c.fetchall()  # get the results of the selection
        count=0
        collection=[]
        #print(mystories)
        while count<len(mystories[0]):
            #print(mystories[0][count])
            if mystories[0][count] != None:
                collection.append(str(mystories[0][count]))
            count+=1
        if len(collection)>0:
            collection=collection[0].split(",")
        #print(collection)
        sorted(collection)
        db.commit()  # save changes
        db.close()  # close database
        if is_admin():
            return render_template('homepage.html', name=session['user'], storycoll=collection)
        return render_template('homepagePEASANT.html', name=session['user'], storycoll=collection)


@app.route("/search")  # search page
def find():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    else:
        return render_template('searchpage.html')


@app.route("/searchresults", methods=["GET", "POST"])  # search results page
def take():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    if session.get('user') is None:  # only give access this page if there's a user
        return redirect(url_for("start"))
    keywords = request.form['keywords']  # retrieve search input
    tags = request.form['tags']
    command = ""
    if keywords == "" and tags == "":  # refresh page is no input but submitted
        return render_template('searchpage.html')
    if len(tags) > 0:  # if tag is inputted, split tag to separate tags
        tags = tags.strip().split(" ")
    if len(keywords) > 0:  # if key words typed in, split keywords into separate tags
        keywords = keywords.strip().split(" ")
        command = "SELECT story_title FROM edits WHERE "  # begin selecting story titles that match keywords
        count = 0
        while count < len(keywords):  # loop through to see if any titles contain the keywords inputted
            if count == len(keywords)-1:
                command += "story_title LIKE \"%" + keywords[count] + "%\""
            else:
                command += "story_title LIKE \"%" + keywords[count] + "%\" OR "
            count += 1
    if len(tags) > 0 and len(keywords) == 0:  # if only tags inputed
        command = "SELECT story_title FROM edits WHERE "  # begin selecting story titles that match tags
        count = 0
        while count < len(tags):  # loop through to see if any stories contain the tags inputted
            if count == len(tags) - 1:
                command += "tags LIKE \"%" + tags[count] + "%\" "
            else:
                command += "tags LIKE \"%" + tags[count] + "%\" OR "
            count += 1
    if len(keywords) > 0 and len(tags) > 0:  # if both search fields are inputted
        count = 0
        while count < len(tags):  # loop through tags because keywords are already searched
            command += " OR tags LIKE \"%"+tags[count]+"%\" "  # loop through to find stories that contained those tags
            count += 1
    command += ";"
    c.execute(command)
    search_results = c.fetchall()  # get the results of the selection
    collection = []
    for item in search_results:
        if str(item) not in collection:
            collection.append(str(item)[2:-3])  # make tuple into strings
    db.commit()  # save changes
    db.close()  # close database
    if is_admin():  # check admin status for different homepages
        return render_template('searchresults.html', key=request.form['keywords'],
                                                     tagged=request.form['tags'],
                                                     results=collection)
    return render_template('searchresultsPEASANT.html', key=request.form['keywords'],
                                                     tagged=request.form['tags'],
                                                     results=collection)


@app.route("/allstories")  # display all stories
def display_all():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    db = sqlite3.connect(DB_FILE)  # open database
    c = db.cursor()
    command = "SELECT story_title from edits"  # get all stories
    c.execute(command)
    all =c.fetchall()  # get the results of the selection
    #print(all)
    count=0
    collection=[]
    while count<len(all):
        #print(all[count][0])
        if all[count][0] != None:
            collection.append(str(all[count][0]))
        count+=1
    ##print(collection)
    sorted(collection)
    db.commit()  # save changes
    db.close()
    if is_admin():
        return render_template('allstory.html', display=collection)
    return render_template('allstoryPEASANT.html', display=collection)


@app.route("/logout")  # log out
def logout():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
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
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    return render_template('storycreator.html')  # new story page


@app.route("/story", methods=["GET", "POST"])  # submission page of new story input
def see_entry():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    title = request.form['story_title']  # retrieve story input
    ##print("this is title:"+title)
    tags = request.form['tags']
    first_entry = request.form['entry_1']
    if title == "" or tags == "" or first_entry == "":  # if there is no input, flash error message and refresh page
        flash("Fill in all the blanks to create a story.")
        return render_template('storycreator.html')
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        created_title = request.form['story_title']
        ##print("createdtitle:"+created_title)
        created_tags = request.form['tags']
        created_entry = request.form['entry_1']
        # insert story input intod database
        command = "INSERT INTO edits VALUES(\"" + created_title + "\",\"" + str(datetime.utcnow()) + \
                  "\",\"" + session['user'] + "\",\"" + created_tags + "\",\'" + created_entry.replace("'","''") + "\');"
        c.execute(command)
        # update users
        command = "SELECT stories_edited FROM users WHERE username = \"" + session['user'] + "\";"
        c.execute(command)
        current_stories_edited = c.fetchall()
        count=0
        edit_total=""
        while count<len(current_stories_edited[0]):
            ##print(current_stories_edited[0][0])
            if current_stories_edited[0][count] != None:
                edit_total+=str(current_stories_edited[0][count])+","
            count+=1
        updated_stores_edited = edit_total+ created_title  # add the new story onto the list
        command = "UPDATE users SET stories_edited=\"" + updated_stores_edited +"\" WHERE username = \"" + session['user'] + "\";"
        c.execute(command)
        command = "SELECT tags FROM edits WHERE story_title=" + "\"" + created_title+ "\";"
        c.execute(command)
        tags = c.fetchall()
        count=0
        tag_coll=[]
        while count<len(tags[0]):
            if tags[0][count] != None:
                tag_coll.append(str(tags[0][count]))
            count+=1
        sorted(tag_coll)
        db.commit()
        db.close()
        created_entry=created_entry.replace("\\'","'")
        return render_template("viewstory.html", title=created_title, entire_story=created_entry,tag_list=tag_coll)


@app.route("/editstory")  # editing page
def queue():
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # finds ip
    ip = request.environ["REMOTE_ADDR"]
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if len(waitlist) == 0 and ip not in waitlist:
        waitlist.append(request.environ["REMOTE_ADDR"])  # if ip is not in waitlist, add it
    command = "SELECT stories_edited FROM users WHERE username = \"" +session.get('user')+"\";"
    c.execute(command)
    editedstories=str(c.fetchall())
    title_save = request.args.get('value')
    command = "SELECT story FROM edits WHERE story_title = \""+title_save+"\";"
    # find the text of a specified story title
    c.execute(command)
    all_edits = c.fetchall()
    all_edits = str(all_edits)[3:-4]  # format string for readability
    command = "SELECT tags FROM edits WHERE story_title=" + "\"" + title_save + "\";"
    c.execute(command)
    # retrieve all the tags for the story
    tags = str(c.fetchall())[3:-4]
    tag_coll = list()
    for tag in tags.split(' '):
        tag_coll.append(str(tag).strip("'"))
    tag_coll = [x for x in tag_coll if x != ""]
    if title_save not in editedstories:
        if waitlist[0] != ip:
            return "Please refresh after "+str(waitlist.index(ip))+" " \
                    "minutes as someone is currently editing."  # calculates place in queue and gives estimate wait time
        else:
            if all_edits.count("|") >= 200:  # if no more edits allowed
                return render_template("viewstory.html", title=title_save, entire_story=all_edits, tag_list=tag_coll)
                # go straight to viewing full story
            else:
                all_edits_list = all_edits.split("|")  # show text without separating pipes
                previous = all_edits_list[-1]
                return render_template("storyeditor.html", previous_edit=previous, title=title_save, tag_list=tag_coll)
    else:
        return render_template("viewstory.html", title=title_save, entire_story=all_edits, tag_list=tag_coll)



@app.route("/viewstory", methods=["GET", "POST"])  # read full story after using story editor
def view():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        new_entry = request.form['new_entry']
        if new_entry == "":
            flash("Please enter something for the new entry.")
            return redirect(url_for("queue"))  # no entry, goes back to editing story
        else:
            # Updates 'story' entry in the table 'edits' for story 'story_title'
            title = request.args.get('value')
            command = "SELECT story FROM edits WHERE story_title =\"" + title + "\";"
            # #print(command)
            c.execute(command)
            current_edits = c.fetchall()
            current_edits = str(current_edits)[3:-4]  # format
            print(new_entry)
            updated_edits = current_edits.replace("'","''") + " | " + new_entry.replace("'","''")  # updated = current + new
            command = "UPDATE edits SET story=\'" + updated_edits + "\' WHERE story_title = \"" + title + "\";"
            print(command)
            c.execute(command)
            #print(command)
            # Updates 'last_editor' entry in table 'edits' for story 'story_title'
            last_editor = session['user']
            command = "UPDATE edits SET last_editor=\"" + last_editor + "\" WHERE story_title = \"" + title + "\";"
            # #print(command)
            c.execute(command)

            # Updates 'timestamp' entry in the table 'edits' for story 'story_title'
            current_time = str(datetime.utcnow())
            command = "UPDATE edits SET time_stamp=\"" + current_time + "\" WHERE story_title =\"" + title + "\";"
            # #print(command)
            c.execute(command)

            # Updates 'stories_edited' entry in the table 'users' for user 'user'
            command = "SELECT stories_edited FROM users WHERE username = \"" + session['user'] + "\";"
            # #print(command)
            c.execute(command)
            current_stories_edited = c.fetchall()
            current_stories_edited = str(current_stories_edited)[3:-4]
            updated_stories_edited = current_stories_edited + "," + title
            command = "UPDATE users SET stories_edited=\"" + updated_stories_edited + \
                      "\" WHERE username = \"" + session['user'] + "\";"
            # #print(command)
            c.execute(command)
            command = "SELECT story FROM edits WHERE story_title =\"" + title + "\";"
            c.execute(command)
            all_edits = c.fetchall()
            entire_story = str(all_edits)[3:-4].replace("\\'","'")

            # retrieves all tags of the story
            command = "SELECT tags FROM edits WHERE story_title=" + "\"" + request.args.get('value') + "\";"
            c.execute(command)
            tags = str(c.fetchall())[3:-4]
            tag_coll = list()
            for tag in tags.split(' '):
                tag_coll.append(str(tag).strip("'"))
            tag_coll = [x for x in tag_coll if x != ""]

            db.commit()
            db.close()
            return render_template("viewstory.html", title=title, entire_story=entire_story, tag_list=tag_coll)


@app.route("/fullstory")  # view full story after clinking on story link
def full():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    else:
        command = "SELECT story FROM edits WHERE " \
                  "story_title = \""+request.args.get('value')+"\";"  # display requested story
        c.execute(command)
        title = request.args.get('value')
        all_edits = c.fetchall()
        try:
            all_edits = str(all_edits[0])[2:-3]
        except IndexError:
            return render_template("deleted.html")
        # retrieves all tags of the story
        command = "SELECT tags FROM edits WHERE story_title=" + "\"" + request.args.get('value') + "\";"
        c.execute(command)
        tags = c.fetchall()
        count=0
        tag_coll=[]
        while count<len(tags[0]):
            if tags[0][count] != None:
                tag_coll.append(str(tags[0][count]))
            count+=1
        if len(tag_coll)>0:
            tag_coll=tag_coll[0].split(",")
        sorted(tag_coll)
        return render_template("viewstory.html", title=title, entire_story=all_edits, tag_list=tag_coll)


@app.route("/close")  # admin power to close a story (no more edits)
def close():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT story FROM edits WHERE story_title = "+"\""+request.args.get('value')+"\";"  # find the story
    print(command)
    c.execute(command)

    view = str(c.fetchall()[0])[2:-3].replace("'","''") # format into string
    command = "UPDATE edits SET story= \'"+view+"|||||||||||||||||||" \
            "|||||||||||||||||||||||||||||||||||||||||||||||||||||||" \
            "|||||||||||||||||||||||||||||||||||||||||||||||||||||||" \
            "||||||||||||||||||||||||||||||||||||||||||||||||||||||||" \
            "|||||||||||||||\'" + " WHERE story_title =" + "\"" + request.args.get('value')+ "\";"
    # add 200 pipes to end editing
    print(command)
    c.execute(command)
    command = "SELECT story FROM edits WHERE story_title = "+"\""+request.args.get('value')+"\";"  # get new story now
    c.execute(command)
    view = str(c.fetchall()[0])[2:-3].replace("\\'","'")
    # retrieve all tags for the story
    command = "SELECT tags FROM edits WHERE story_title=" + "\"" + request.args.get('value') + "\";"
    c.execute(command)
    tags = str(c.fetchall())[3:-4]
    tag_coll = list()
    for tag in tags.split(' '):
        tag_coll.append(str(tag).strip("'"))
    tag_coll = [x for x in tag_coll if x != ""]
    db.commit()
    db.close()
    return render_template("closestory.html", title=request.args.get('value'), entire_story=view, tag_list=tag_coll)
    # displays story by replacing all | with empty string


@app.route("/tagedit")  # admin power to edit a story's tags
def edit_tags():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    story_name = request.args.get('value')  # get story title
    command = "SELECT tags FROM edits WHERE story_title=" + "\"" + story_name + "\";"  # retrieve all tags for the story
    c.execute(command)
    tags = str(c.fetchall())[3:-4]
    tag_coll = list()
    for tag in tags.split(' '):
        tag_coll.append(str(tag).strip("'"))
    tag_coll = [x for x in tag_coll if x != ""]
    return render_template("tagedit.html", tag_list=tag_coll, story_title=story_name)


@app.route("/addtag", methods=['GET', 'POST'])  # admin power to add tags to a story
def add_tag():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    title=str(request.args.get('story')).replace('"','')
    command = "SELECT tags FROM edits WHERE story_title = " + "\"" + title+ "\";"  # retrieve all tags for the story
    # find the whole story
    # #print(command)
    c.execute(command)
    tags =c.fetchall()  # get the results of the selection
    count=0
    collection=[]
    #print(tags)
    while count<len(tags[0]):
        #print(tags[0][count])
        #print(tags[0][count])
        if tags[0][count] != None:
            collection.append(str(tags[0][count]))
        count+=1
    if len(collection)>0:
        collection=collection[0].split(" ")
        tag_coll_str=" ".join(collection)
    newtag = str(request.form.get('new_tags'))  # retrieve input for new tags
    if len(newtag)>0 and newtag[0] != "#":
        newtag = "#" + newtag
    if newtag not in tag_coll_str:
        command = "UPDATE edits SET tags= \"" + tag_coll_str + " " + newtag + "\"" + \
                "WHERE story_title ="+"\""+title+"\";"  # add new tags to list of tags
        # #print(command)
        c.execute(command)
        db.commit()
        db.close()
    return redirect(url_for('story'))


@app.route("/deletetag")  # admin power to delete tags of a story
def delete_tag():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    story_name = request.args.get('story')  # retrieve story information
    tag_name = request.args.get('tag')
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # retrieve all tags for a story
    command = "SELECT tags FROM edits WHERE story_title=" + "\"" + story_name + "\";"
    c.execute(command)
    tags =c.fetchall()  # get the results of the selection
    count=0
    collection=[]
    #print(tags)
    while count<len(tags[0]):
        #print(tags[0][count])
        #print(tags[0][count])
        if tags[0][count] != None:
            collection.append(str(tags[0][count]))
        count+=1
    if len(collection)>0:
        collection=collection[0].split(" ")
        #print(collection)
        #print(tag_name)
        collection.remove(tag_name)
        #print(collection)
        tag_coll_str=" ".join(collection)
        #print(tag_coll_str)
    # update tags list after deletion
    command = "UPDATE edits SET tags=" + "\"" + tag_coll_str + "\"" + " WHERE story_title=" + "\"" + story_name + "\";"
    c.execute(command)
    db.commit()
    db.close()
    return redirect(url_for('story'))


@app.route("/delete")  # admin power to delete a story
def delete():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # remove from queue
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "DELETE FROM edits WHERE story_title = \""+request.args.get('value')+"\";"  # delete entire row from edits
    c.execute(command)
    db.commit()
    db.close()
    return render_template("deletestory.html", title=request.args.get('value'))


@app.route("/updateprofile")  # users allowed to change user or password
def update():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove(ip)
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    else:  # otherwise go to profile change page
        return render_template('editprofile.html')


@app.route("/updateprofilecheck", methods=["GET", "POST"])  # retrieving input and checking user's desired changes to profil
def update_check():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ["REMOTE_ADDR"]
    if ip in waitlist:
        waitlist.remove()
    if session.get('user') is None:  # only give access to this page if there's a user
        return redirect(url_for("start"))
    old_username = request.form['old_username']  # retrieve html form information
    old_password = request.form['old_password']
    username = request.form['new_username']
    password = request.form['new_password']
    password_again = request.form['passwordagain']
    # if user wants to change username
    if request.form.get('change_user'):
        if (username and old_username == "") or (username == "" and old_username):  # check if both fields are inputted
            flash("Please fill in both your old and new information to update your profile.")
            return render_template('editprofile.html')
        if username == old_username:  # check if old and new username is the same
            flash("Your old and new username are the same. Nothing will be changed.")
            return render_template('editprofile.html')
        #print(check_sign(old_username))
        if check_sign(old_username) != "done":  # if the old username is correct...
            check = check_sign(username)  # check if new username is valid
            if check != "done":   # if it isn't valid, flash error message
                flash("" + check)
                return render_template('editprofile.html')
            else:  # otherwise, change username
                edit_name(old_username, username)
                session['user'] = username  # change session name
                if not(request.form.get('change_pwd')):
                    flash("Your username has been updated.")
                    return render_template('editprofile.html')
        else:
            flash("Old username is incorrect.")
            return render_template('editprofile.html')
    # if user wants to change password
    if request.form.get('change_pwd'):
        if (password and old_password) == "" or (password == "" and old_password):
            # check if both fields are inputted
            flash("Please fill in both your old and new information to update your profile.")
            return render_template('editprofile.html')
        if password == old_password:  # check if old and new password are the same
            flash("Your old and new password are the same. Nothing will be changed.")
            return render_template('editprofile.html')
        check = check_pwd(session['user'], old_password)  # check if old password is correct
        if check != "done":
            flash("" + check)
            return render_template('editprofile.html')
        else:
            if password != password_again:  # check if both passwords match
                flash("Password does not match.")
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
