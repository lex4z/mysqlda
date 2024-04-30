import mysql.connector as mc
import tkinter as tk
import json

with open("config.json") as f:
    config = json.load(f)

db = mc.connect(**config)

cursor = db.cursor()
cursor.execute("SELECT Educational_Track_Name FROM oop")
oop_names = [i[0] for i in cursor]

print(oop_names)
