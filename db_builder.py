#Team Printer Carts
#SoftDev

import sqlite3   #enable control of an sqlite database

DB_FILE= "foldoverdata.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#================================================

#"users" Databse
#This database is for storing user information and permissions
	#username TEXT: user's username
	#password TEXT: user's password
	#stories_edited: history of all created and edited stories
	#is_admin: 1 if admin, 0 if not
command = "CREATE TABLE users (username TEXT, password TEXT, stories_edited BLOB, is_admin INTEGER)"
c.execute(command)

#(Main) Database Story Attribute
#This database is for storing information about the stories itself
	#story_title TEXT: the title of the story
	#time_stamp TIME: the time story was last edited
	#last_editor TEXT: the last editor of the story
	#tags TEXT: tags for stories for easier search and categorization
	#story BLOB: the HTML of the whole story, to be displayed
command = "CREATE TABLE stories (story_title TEXT, time_stamp TIME, last_editor TEXT, tags TEXT, story BLOB)"
c.execute(command)
#================================================
db.commit()
db.close()
