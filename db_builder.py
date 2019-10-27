#Team Printer Carts
#SoftDev

import sqlite3   #enable control of an sqlite database
import csv

DB_FILE= "data/foldoverdata.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#================================================

#"users" table
command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, stories_edited TEXT, is_admin BOOLEAN)"
c.execute(command)

csvfile = open('data/userdata.csv', newline='')
reader = csv.DictReader(csvfile)
for row in reader:
	command = 'INSERT INTO users VALUES(\"' + row['username'] + '\",\"' + row['password'] + '\",\"' + row['stories_edited'] + '\",' + row['is_admin'] + ')'
	print(command)
	c.execute(command)

#"edits" table
command = "CREATE TABLE IF NOT EXISTS edits (story_title TEXT, time_stamp BLOB, last_editor TEXT, tags TEXT, story TEXT)"
c.execute(command)

csvfile = open('data/editdata.csv', newline='')
reader = csv.DictReader(csvfile)
for row in reader:
	command = 'INSERT INTO edits VALUES(\"' + row['story_title'] + '\",\"' + row['time_stamp'] + '\",\"' + row['last_editor'] + '\",\"' + row['tags'] + '\",\"' + row['story'] + '\")'
	print(command)
	c.execute(command)

#================================================
db.commit()
db.close()
