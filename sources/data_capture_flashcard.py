import sqlite3
from pathlib import Path
import configparser, os
from tkinter import StringVar, messagebox

TEST_ROW = 16

file_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
db = file_root + os.path.sep + "MagicRoom.db"


def get_Images(lesson_id_list):

    connection = sqlite3.connect(db)
    cur = connection.cursor()
    lesson_id_tuple = tuple(lesson_id_list)
    if len(lesson_id_tuple) == 1:
        sql = "select Lesson_ID,Factual_Image1,Factual_Image2,Factual_Image3 from Magic_Science_Lessons where Lesson_ID is ?"
        cur.execute(sql, (lesson_id_tuple[0],))
    else:
        sql = "select Lesson_ID, Factual_Image1,Factual_Image2,Factual_Image3 from Magic_Science_Lessons where Lesson_ID in {}".format(lesson_id_tuple)
        cur.execute(sql)
    images = cur.fetchall()
    connection.commit()
    connection.close()
    return images

def get_Fact_Terms(lesson_id_list):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    lesson_id_tuple = tuple(lesson_id_list)
    if len(lesson_id_tuple) == 1:
        sql = "select Factual_Term1, Factual_Term2, Factual_Term3 from Magic_Science_Lessons where Lesson_ID is ?"
        cur.execute(sql,(lesson_id_tuple[0], ))

    else:
        sql = "select Factual_Term1, Factual_Term2, Factual_Term3 from Magic_Science_Lessons where Lesson_ID in {}".format(lesson_id_tuple)
        cur.execute(sql)
    terms = cur.fetchall()
    # print(text)
    connection.commit()
    connection.close()
    return terms

def get_Fact_Descriptions(lesson_id_list):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    lesson_id_tuple = tuple(lesson_id_list)
    if len(lesson_id_tuple) == 1:
        sql = "select Factual_Term1_Description, Factual_Term2_Description, Factual_Term3_Description from Magic_Science_Lessons where Lesson_ID is ?"
        cur.execute(sql, (lesson_id_tuple[0],))
    else:
        sql = "select Factual_Term1_Description, Factual_Term2_Description, Factual_Term3_Description from Magic_Science_Lessons where Lesson_ID in {}".format(lesson_id_tuple)
        cur.execute(sql)
    descriptions = cur.fetchall()
    connection.commit()
    connection.close()
    return descriptions

def get_Lessons():
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID, Lesson_Title from Magic_Science_Lessons"
    cur.execute(sql)
    rows = cur.fetchall()
    list_lessons = []
    for element in rows:
        list_lessons.append(element)
    connection.commit()
    connection.close()
    return list_lessons

def class_info():
    list_names = []
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select * from Magic_Class_Info"
    cur.execute(sql)
    rows = cur.fetchall()
    for element in rows:
        list_names.append(element)

    connection.commit()
    connection.close()
    return list_names



def save_leader_board_data(list_points):
    connection = sqlite3.connect(db)
    cur = connection.cursor()

    for element in list_points:
        sql = "select Badge_A_Threshold, Badge_B_Threshold, Badge_C_Threshold from Magic_Class_Info where Name=?"
        badge_info_c = cur.execute(sql, (element[0],))
        badge_info = badge_info_c.fetchone()
        badge_a = badge_info[0]
        badge_b = badge_info[1]
        badge_c= badge_info[2]
        var = StringVar()
        var = element[1]
        value = var.get()
        badge = ''
        if int(value) > badge_a:
            badge = 'a'
        elif int(value) > badge_b:
            badge ='b'
        elif int(value) > badge_c:
            badge = 'c'
        sql='update Magic_Class_Info set Points = ? , Badge = ? where Name=?'
        print(value,element[0])
        cur.execute(sql,(int(value), badge, element[0]))

    connection.commit()
    connection.close()

def get_experiment_content(lesson_id):
    imageroot = file_root + os.path.sep + "Lessons"+os.path.sep+"Lesson"+str(lesson_id)+os.path.sep+"images"+os.path.sep
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()

        sql = (
            'select Application_Steps_Number, Application_Step_Description_1, Application_Step_Description_2, Application_Step_Description_3,'
            'Application_Step_Description_4,Application_Step_Description_5,Application_Step_Description_6,Application_Step_Description_7'
            ',Application_Step_Description_8,Application_Steps_Widget_1,Application_Steps_Widget_2,Application_Steps_Widget_3,Application_Steps_Widget_4'
            ',Application_Steps_Widget_5,Application_Steps_Widget_6,Application_Steps_Widget_7,Application_Steps_Widget_8 from Magic_Science_Lessons '
            'where Lesson_ID = ?')
        experiment_info_c = cur.execute(sql, (lesson_id,))
        experiment_info = experiment_info_c.fetchone()
        # print(experiment_info)
        experiment_steps = [experiment_info[1], experiment_info[2], experiment_info[3], experiment_info[4],
                            experiment_info[5], experiment_info[6], experiment_info[7], experiment_info[8]]
        experiment_images = [imageroot + experiment_info[9], imageroot + experiment_info[10],
                             imageroot + experiment_info[11], imageroot + experiment_info[12],
                             imageroot + experiment_info[13], imageroot + experiment_info[14],
                             imageroot + experiment_info[15], imageroot + experiment_info[16]]
        experiment_steps_total = experiment_info[0]
        connection.close()
        return experiment_steps, experiment_images, experiment_steps_total
    except sqlite3.OperationalError:
        messagebox.showerror("DB Error", "Cannot Connect to Database")
