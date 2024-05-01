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

print(oop_ids)

def drop1_selected(event):
    btn1.config(state="normal")
    btn1.focus_force()

'''
def drop1_check_input(event):
    
    request = drop1_text.get()

    if request != "":
        found_oop_ids = []
        for i in oop_ids[1]:
            if request.lower() in i.lower(): 
                found_oop_ids.append(i)
        drop1['values'] = found_oop_ids
    else:
        drop1['values'] = oop_ids[1]
'''

def btn1_click():
    return

drop1_text = tk.StringVar()

lbl1 = tk.Label(root, text = "Выберите ООП")
lbl1.pack()

drop1 = ttk.Combobox(root, values = oop_ids[1], textvariable = drop1_text, state="readonly", width=70)
drop1.bind("<<ComboboxSelected>>", drop1_selected)
#drop1.bind("<KeyRelease>",drop1_check_input)
drop1.pack()

btn1 = tk.Button(root, text = "Start",state = "disabled", command=btn1_click)
btn1.pack()


root.mainloop()

