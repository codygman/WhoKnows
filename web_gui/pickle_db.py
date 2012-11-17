import pickle
import sqlite3
import json

#sqlite db setup
con = sqlite3.connect('professors.db')
cur = con.cursor()
professors = []

cur.execute("select id, name, email, image_url, dept from professors")
rows = cur.fetchall()
for row in rows:
    id = row[0]
    email = row[1]
    image_url = row[2]
    dept = row[3]

    professor = {'id' : int(id), 'email' : email, 'image_url' : image_url, 'dept' : dept}
    professors.append(professor)

f = open('professors.pp', 'wb')
pickle.dump(professors, f)
