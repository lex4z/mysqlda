import mysql.connector as mc
import tkinter as tk
from tkinter import ttk
import json

with open("config.json") as f:
    config = json.load(f)

db = mc.connect(**config)

root = tk.Tk()
root.title("window")
root.geometry("400x200")

cursor = db.cursor()
cursor.execute("SELECT Educational_Track_Name, Educational_Programm_Name FROM oop ORDER BY Educational_Programm_Name")

et_names = []
oop_names = []
oop_ids = []

for (i,j) in cursor:
    et_names.append(i)
    oop_names.append(j)

cursor.execute("SELECT ID_OOP FROM real_oop ORDER BY Educational_Programm_Name")
oop_ids = [i[0] for i in cursor]

print(et_names,oop_names,oop_ids)

def show(event):
    lbl1.config(text = drop.get())

clicked = tk.StringVar()
#drop = tk.OptionMenu(root, clicked, *oop_names, command=show)

drop = ttk.Combobox(root, values = et_names, textvariable = clicked,state = "readonly")
drop.pack()
drop.bind("<<ComboboxSelected>>", show)

#btn = tk.Button(root, text = "reload", command=show).pack()

lbl1 = tk.Label(root, text = " ")
lbl1.pack()

root.mainloop()
#print(oop_names)
