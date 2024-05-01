import mysql.connector as mc
import tkinter as tk
from tkinter import ttk
import json

with open("config.json") as f:
    config = json.load(f)

db = mc.connect(**config)

root = tk.Tk()
root.title("window")
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()

window_width = 500
window_height = 300

root.geometry(f"{window_width}x{window_height}")

cursor = db.cursor()
cursor.execute("SELECT ID_OOP,Educational_Programm_Name FROM real_oop ORDER BY Educational_Programm_Name")

oop_ids = [[],[]] #oop_ids[0] - ID_OOP oop_ids[1] - oop_name[id]

for (i,j) in cursor:
    oop_ids[0].append(i)
    oop_ids[1].append(j)

cursor.execute("SELECT Discipline_ID,Discipline_laboratory,Discipline_lectures,Discipline_practices FROM rpd WHERE stavka_part = 0")
temp = [[],[]]
for (id, dlab, dlect, dpract) in cursor:
    temp[0].append(id)
    temp[1].append(round((dlab+dlect+dpract)/900,2))

for i in range(len(temp[0])):
    cursor.execute("UPDATE rpd SET stavka_part = " + str(temp[1][i]) + " WHERE Discipline_ID = " + str(temp[0][i]))
    db.commit()

def drop1_selected(event):
    btn1.config(state="normal")
    btn1.focus_force()

def btn1_click():
    selected_oop_id = oop_ids[0][oop_ids[1].index(drop1_text.get())]
    cursor.execute(f"SELECT stavka_part FROM rpd WHERE ID_OOP = {selected_oop_id}")
    all_sum = sum([i[0] for i in cursor])

    cursor.execute(f"SELECT stavka_part FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_academic_degree != 'нет' AND rpd.ID_OOP = {selected_oop_id}")
    partial_sum = sum([i[0] for i in cursor])
    n1 = round(100*partial_sum/all_sum,2)

    cursor.execute(f"SELECT stavka_part FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_practice_type = 'да' AND rpd.ID_OOP = {selected_oop_id}")
    partial_sum = sum([i[0] for i in cursor])
    n2 = round(100*partial_sum/all_sum,2)

    lbl2.config(text=f"Рассчет показателей для ООП {drop1_text.get()}\n Остепененность: {n1}%\n Практики: {n2}%")

    return

drop1_text = tk.StringVar()

lbl1 = tk.Label(root, text = "Выберите ООП")
lbl1.pack()

drop1 = ttk.Combobox(root, values = oop_ids[1], textvariable = drop1_text, state="readonly", width=70)
drop1.bind("<<ComboboxSelected>>", drop1_selected)
drop1.pack()

btn1 = tk.Button(root, text = "Start",state = "disabled", command=btn1_click)
btn1.pack()

lbl2 = tk.Label(root, text="",width=65,wraplength=450)
lbl2.pack()


root.mainloop()

