import mysql.connector as mc
import tkinter as tk
from tkinter import ttk
import json

with open("config.json") as f:
    config = json.load(f)

db = mc.connect(**config)

root = tk.Tk()
root.title("window")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width*0.2)
window_height = int(screen_height*0.3)

root.geometry(f"{window_width}x{window_height}")

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

def dropSelectd(event):
    lbl1.config(text = drop.get())

clicked = tk.StringVar()

#drop = tk.OptionMenu(root, clicked, *oop_names, command=show)

lbl1 = tk.Label(root, text = "Выберите направление")
lbl1.pack()

drop = ttk.Combobox(root, values = et_names, textvariable = clicked,state = "readonly",width=40)
drop.pack()
drop.bind("<<ComboboxSelected>>", dropSelectd)

#btn = tk.Button(root, text = "reload", command=show).pack()



root.mainloop()

