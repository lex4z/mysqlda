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

def oop_selected(event):
    clear_buttons()
    lbl2.config(text="")
    get_project_indicators_btn.config(state="normal")
    get_real_indicators_btn.config(state="normal")

def clear_buttons():
    recomendations_label.pack_forget()
    get_recomendations_btn.pack_forget()
    get_disciplines_frame.pack_forget()
    #get_teachers_disciplines_btn.pack_forget()

def get_project_indicators():
    clear_buttons()
    
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

    project_indicators += f"Доля работников из числа руководителей и(или) работников организаций, деятельность которых связана с направленностью реализуемой ОП: {n2}% - {is_valid2} соответствует требованиям(более {pract_percent}%)"
    
    lbl2.config(justify=tk.LEFT,text=project_indicators)

    if(is_valid1 + is_valid2!=''): get_recomendations_btn.pack()
    
    return


def get_recomendations():
    global display_n1, display_n2
    display_n1 = False
    display_n2 = False
    recomendations = "Для соответствия показателей:\n"
    if n1 < ost_percent:
        display_n1 = True
        n_ost = ceil(all_hours*ost_percent/100)
        n_ost += n_ost%2
        recomendations += f"необходимо передать {n_ost-degree_hours} часа(ов) преподователю(ям) со степенью\n"

    if n2 < pract_percent:
        display_n2 = True
        n_pract = ceil(all_hours*pract_percent/100)
        n_pract += n_pract%2
        recomendations += f"необходимо передать {n_pract-pract_hours} часа(ов) преподователю(ям)-практику(ам)\n"
    
    recomendations_label.config(justify=tk.LEFT,text=recomendations)
    recomendations_label.pack()
    get_up_disciplines_btn.pack(side='left')
    get_teachers_disciplines_btn.pack(side='right')
    get_disciplines_frame.pack()
    return

def get_up_disciplines():
    selected_oop_id = oop_ids[oop_drop_text.get()]
    cursor.execute(f"SELECT Discipline_name,Discipline_laboratory,Discipline_lectures,Discipline_practices,Discipline_intensity FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_academic_degree != 'нет' AND rpd.ID_OOP = {selected_oop_id}")
    degree_disciplines = [i for i in cursor]

    cursor.execute(f"SELECT Discipline_name,Discipline_laboratory,Discipline_lectures,Discipline_practices,Discipline_intensity FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_practice_type = 'да' AND rpd.ID_OOP = {selected_oop_id}")
    pract_disciplines = [i for i in cursor]

    names = ("Наименование дисциплины","Лабораторные","Лекции","Практики","Трудоёмкость")
    tree_columns=("Discipline_name","Discipline_laboratory","Discipline_lectures","Discipline_practices","Discipline_intensity")
    tree_widths = (500,100,100,100,100)
    text1 = "Дисциплины, закреплённые за остепенёнными преподователями, которые соответствуют требованиям"
    text2 = "Дисциплины, закреплённые за преподователями-практиками, которые соответствуют требованиям"
    window_size = "900x500"

    create_window_with_data(degree_disciplines,pract_disciplines,text1,text2,names,tree_columns,tree_widths,'результат "Исправить УП"',window_size,display_n1,display_n2)
    return

def get_teachers_disciplines():
    selected_oop_id = oop_ids[oop_drop_text.get()]
    cursor.execute(f"SELECT Discipline_name,Discipline_laboratory,Discipline_lectures,Discipline_practices,Discipline_intensity FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_academic_degree = 'нет' AND rpd.ID_OOP = {selected_oop_id}")
    degree_disciplines = [i for i in cursor]

    cursor.execute(f"SELECT Discipline_name,Discipline_laboratory,Discipline_lectures,Discipline_practices,Discipline_intensity FROM rpd, teachers, tea_dis WHERE rpd.Discipline_ID = tea_dis.Discipline_ID AND tea_dis.Teacher_ID = teachers.Teacher_ID AND teachers.Teacher_practice_type != 'да' AND rpd.ID_OOP = {selected_oop_id}")
    pract_disciplines = [i for i in cursor]

    names = ("Наименование дисциплины","Лабораторные","Лекции","Практики","Трудоёмкость")
    tree_columns=("Discipline_name","Discipline_laboratory","Discipline_lectures","Discipline_practices","Discipline_intensity")
    tree_widths = (500,100,100,100,100)
    text1 = "Дисциплины, закреплённые за остепенёнными преподователями, которые НЕ соответствуют требованиям"
    text2 = "Дисциплины, закреплённые за преподователями-практиками, которые НЕ соответствуют требованиям"
    window_size = "900x500"

    create_window_with_data(degree_disciplines,pract_disciplines,text1,text2,names,tree_columns,tree_widths,'результат "Исправить преподователей"',window_size,display_n1,display_n2)
    return

def create_window_with_data(data1,data2,text1,text2,names,columns,widths,title,window_size,display_data1,display_data2):
    result_window = tk.Tk()
    result_window.title(title)
    result_window.geometry(window_size)

    if(display_data1 == True):
        rw_lbl1 = tk.Label(result_window, text=text1).pack()

        tree1 = ttk.Treeview(result_window, columns=columns, show="headings")
        
        for i in range(len(names)): 
            tree1.column(i,stretch=False,width=widths[i])
            tree1.heading(i,text=names[i])

        for data in data1:
            tree1.insert("",tk.END,values=data)
        
        tree1.pack()

    if(display_data2 == False): return

    rw_lbl2 = tk.Label(result_window, text=text2).pack()

    tree2 = ttk.Treeview(result_window, columns=columns, show="headings")
    
    for i in range(len(names)): 
        tree2.column(i,stretch=False,width=widths[i])
        tree2.heading(i,text=names[i])

    for data in data2:
        tree2.insert("",tk.END,values=data)
    
    tree2.pack()

def get_real_indicators():
    clear_buttons()

    cursor.execute(f"SELECT Students_number, Students_number_real FROM oop WHERE Educational_Programm_Name = '{oop_drop_text.get()}'")
    students_num = [i for i in cursor]
    cursor.execute(f"SELECT Students_job, Students_job_real FROM oop WHERE Educational_Programm_Name = '{oop_drop_text.get()}'")
    students_job_num = [i for i in cursor]
    students_num = students_num[0]
    students_job_num = students_job_num[0]
    
    n1_real = students_num[1]/students_num[0]
    n2_real = students_job_num[1]/students_job_num[0]
    
    real_indicators =  f"Рассчет показателей реализации для ООП {oop_drop_text.get()}\n\n"
    
    risk = ''
    if(n1<0.9):
        risk = 'показатель не соответствует требованиям (процент отчисления студентов превышает 10%)'
    elif(n1<0.92):
        risk = 'показатель отчисления студентов в зоне риска (8-10% от КЦП)'
    else:
        risk = 'показатель соответствует требованиям (процент отчисления студентов менее 10% от КЦП)'
    
    real_indicators += f"Сохранность контингента: {round(n1_real*100,2)}%\n{risk}\n\n"

    real_indicators += f"Процент трудоустроенных в течении одного года после окончания обучения: {round(n2_real*100,2)}%"
    
    lbl2.config(justify=tk.LEFT,text=real_indicators)
    return

oop_drop_text = tk.StringVar() 

lbl1 = tk.Label(root, text = "Выберите ООП")
lbl1.pack()

oop_drop = ttk.Combobox(root, values = list(oop_ids.keys()), textvariable = oop_drop_text, state="readonly", width=70)
oop_drop.bind("<<ComboboxSelected>>", oop_selected)
oop_drop.pack()

get_indicators_frame = tk.Frame(root)

get_project_indicators_btn = tk.Button(get_indicators_frame, text = "показатели проектирования",state = "disabled", command=get_project_indicators,width=30)
get_project_indicators_btn.pack(side='left')

get_real_indicators_btn = tk.Button(get_indicators_frame, text = "показатели реализации",state = "disabled", command=get_real_indicators,width=30)
get_real_indicators_btn.pack(side='right')
get_indicators_frame.pack()

lbl2 = tk.Label(root, text="",width=80,wraplength=570)
lbl2.pack()

get_recomendations_btn = tk.Button(root, text = "Предложить рекомендации", command=get_recomendations)
recomendations_label = tk.Label(root, text="",width=80,wraplength=570)

get_disciplines_frame = tk.Frame(root)

get_up_disciplines_btn = tk.Button(get_disciplines_frame, text="Исправить УП",command=get_up_disciplines,width=30)
get_teachers_disciplines_btn = tk.Button(get_disciplines_frame, text="Исправить преподавателей",command=get_teachers_disciplines,width=30)





root.mainloop()

