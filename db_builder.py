import sqlite3   #enable control of an sqlite database

DB_FILE= "foldoverdata.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, stories_edited BLOB, is_admin INTEGER)"
c.execute(command)

db.commit()
db.close()
