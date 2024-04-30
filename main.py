import mysql.connector as mc
import json


_host = "localhost"
_user = "root"
_password = ""
_database = "anna"

db = mc.connect(
    host = _host,
    user = _user,
    password = _password,
    database = _database
)

cursor = db.cursor()
cursor.execute("SELECT Educational_Track_Name FROM oop")
oop_names = [i[0] for i in cursor]

print(oop_names)
