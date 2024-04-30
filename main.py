import mysql.connector as mc
import tkinter as tk
import json

with open("config.json") as f:
    config = json.load(f)

db = mc.connect(**config)

root = tk.Tk()
root.title("window")


cursor = db.cursor()
cursor.execute("SELECT Educational_Track_Name FROM oop")
oop_names = [i[0] for i in cursor]

def show(text):
    lbl1.config(text = text)

clicked = tk.StringVar()
drop = tk.OptionMenu(root, clicked, *oop_names, command=show)
drop.pack()

#btn = tk.Button(root, text = "reload", command=show).pack()

lbl1 = tk.Label(root, text = " ")
lbl1.pack()

root.mainloop()
#print(oop_names)
