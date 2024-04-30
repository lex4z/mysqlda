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
cursor.execute("SELECT Educational_Track_Name FROM oop WHERE Admission_year>0")
oop_names = [i for i in cursor]
#oop_names = oop_names[2:]

print(oop_names)


'''
cursor = db.cursor()

cursor.execute("SHOW DATABASES")
for i in cursor:
    print(i)

'''