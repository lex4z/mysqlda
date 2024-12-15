import mysql.connector as mc
import tkinter as tk
from tkinter import ttk
from math import ceil
import json

with open("config.json") as f:
    config = json.load(f)

global ost_percent, pract_percent
ost_percent = config.pop("ost_percent")
pract_percent = config.pop("pract_percent")



db = mc.connect(**config)

root = tk.Tk()
root.title("window")
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()

window_width = 700
window_height = 400

root.geometry(f"{window_width}x{window_height}")

cursor = db.cursor()
cursor.execute("SELECT ID_OOP,Educational_Programm_Name FROM real_oop ORDER BY Educational_Programm_Name")

oop_ids = [] 

for (i,j) in cursor:
    oop_ids.append([j,i])
oop_ids = dict(oop_ids)

cursor.execute("SELECT Discipline_ID,Discipline_laboratory,Discipline_lectures,Discipline_practices FROM rpd WHERE stavka_part = 0")
temp = [[],[]]
for (id, dlab, dlect, dpract) in cursor:
    temp[0].append(id)
    temp[1].append(round((dlab+dlect+dpract)/900,10))

for i in range(len(temp[0])):
    cursor.execute(f"UPDATE rpd SET stavka_part = {temp[1][i]} WHERE Discipline_ID = {temp[0][i]}")
    db.commit()

def oop_selected(event):
    get_project_indicators_btn.config(state="normal")
    get_real_indicators_btn.config(state="normal")
    #get_project_indicators_btn.focus_force()


def get_project_indicators():
    recomendations_label.pack_forget()
    get_recomendations_btn.pack_forget()
    global all_hours, degree_hours, pract_hours, n1, n2
    selected_oop_id = oop_ids[oop_drop_text.get()]
    cursor.execute(f"SELECT Discipline_laboratory,Discipline_lectures,Discipline_practices FROM rpd WHERE ID_OOP = {selected_oop_id}")
    all_hours = sum([sum(i) for i in cursor])

    cursor.execute(f"SELECT Discipline_laboratory,Discipline_lectures,Discipline_practices FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_academic_degree != 'нет' AND rpd.ID_OOP = {selected_oop_id}")
    degree_hours = sum([sum(i) for i in cursor])
    n1 = round(100*degree_hours/all_hours,2)

    cursor.execute(f"SELECT Discipline_laboratory,Discipline_lectures,Discipline_practices FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_practice_type = 'да' AND rpd.ID_OOP = {selected_oop_id}")
    pract_hours = sum([sum(i) for i in cursor])
    n2 = round(100*pract_hours/all_hours,2)

    
    project_indicators = f"Рассчет показателей пректирования для ООП {oop_drop_text.get()}\n\n" 
    is_valid1 = ''
    if n1 < ost_percent: is_valid1 = 'НЕ'
    project_indicators += f"Доля научно-педагогических работников, имеющих ученую степень: {n1}% - {is_valid1} соответствует требованиям (более {ost_percent}%)\n\n"

    is_valid2 = ''
    if n2 < pract_percent: is_valid2 = 'НЕ'

    project_indicators += f"Доля работников из числа руководителей и(или) работников организаций, деятельность которых связана с направленностью реализуемой ОП: {n2}% = {is_valid2} соответствует требованиям(более {pract_percent}%)"
    
    lbl2.config(justify=tk.LEFT,text=project_indicators)

    if(is_valid1 + is_valid2!=''): get_recomendations_btn.pack()
    
    return


def get_recomendations():
    recomendations_label.pack_forget()
    recomendations = "Для соответствия показателей:\n"
    if n1 < ost_percent:
        n_ost = ceil(all_hours*ost_percent/100)
        n_ost += n_ost%2
        recomendations += f"необходимо передать {n_ost-degree_hours} часа(ов) преподователю(ям) со степенью\n"

    if n2 < pract_percent:
        n_pract = ceil(all_hours*pract_percent/100)
        n_pract += n_pract%2
        recomendations += f"необходимо передать {n_pract-pract_hours} часа(ов) преподователю(ям)-практику(ам)\n"

    
    recomendations_label.config(justify=tk.LEFT,text=recomendations)
    recomendations_label.pack()
    return

def get_real_indicators():
    recomendations_label.pack_forget()
    get_recomendations_btn.pack_forget()
    
    cursor.execute(f"SELECT Students_number, Students_number_real FROM oop WHERE Educational_Programm_Name = '{oop_drop_text.get()}'")
    students_num = [i for i in cursor]
    cursor.execute(f"SELECT Students_job, Students_job_real FROM oop WHERE Educational_Programm_Name = '{oop_drop_text.get()}'")
    students_job_num = [i for i in cursor]
    students_num = students_num[0]
    students_job_num = students_job_num[0]
    
    n1 = students_num[1]/students_num[0]
    n2 = students_job_num[1]/students_job_num[0]
    
    real_indicators =  f"Рассчет показателей реализации для ООП {oop_drop_text.get()}\n\n"
    
    risk = ''
    if(n1<0.9):
        risk = 'показатель отчисления студентов превышает 10% от КЦП'
    elif(n1<0.92):
        risk = 'показатель отчисления студентов в зоне риска (8-10% от КЦП)'
    else:
        risk = 'показатель соответствует требованиям (процент отчисления студентов менее 10% от КЦП)'
    
    real_indicators += f"Сохранность контингента: {round(n1*100,2)}%\n{risk}\n\n"

    real_indicators += f"Процент трудоустроенных в течении одного года после окончания обучения: {round(n2*100,2)}%"
    
    lbl2.config(justify=tk.LEFT,text=real_indicators)
    return

oop_drop_text = tk.StringVar() 

lbl1 = tk.Label(root, text = "Выберите ООП")
lbl1.pack()

oop_drop = ttk.Combobox(root, values = list(oop_ids.keys()), textvariable = oop_drop_text, state="readonly", width=70)
oop_drop.bind("<<ComboboxSelected>>", oop_selected)
oop_drop.pack()

get_project_indicators_btn = tk.Button(root, text = "показатели проектирования",state = "disabled", command=get_project_indicators,width=30)
get_project_indicators_btn.pack()

get_real_indicators_btn = tk.Button(root, text = "показатели реализации",state = "disabled", command=get_real_indicators,width=30)
get_real_indicators_btn.pack()

lbl2 = tk.Label(root, text="",width=80,wraplength=570)
lbl2.pack()

get_recomendations_btn = tk.Button(root, text = "Предложить рекомендации", command=get_recomendations)


recomendations_label = tk.Label(root, text="",width=80,wraplength=570)


root.mainloop()

