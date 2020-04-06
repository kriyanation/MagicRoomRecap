import sqlite3
from pathlib import Path
import configparser
from tkinter import StringVar
TEST_ROW = 16

config = configparser.RawConfigParser()
two_up = Path(__file__).absolute().parents[2]
print(str(two_up)+'/magic.cfg')
config.read(str(two_up)+'/magic.cfg')

db = config.get("section1",'dataroot')
imageroot = config.get("section1",'image_root')
videoroot = config.get("section1",'video_root')

def get_Images(lesson_id_list):

    connection = sqlite3.connect(db)
    cur = connection.cursor()
    lesson_id_tuple = tuple(lesson_id_list)
    if len(lesson_id_tuple) == 1:
        sql = "select Factual_Image1,Factual_Image2,Factual_Image3 from Magic_Science_Lessons where Lesson_ID is ?"
        cur.execute(sql, (lesson_id_tuple[0],))
    else:
        sql = "select Factual_Image1,Factual_Image2,Factual_Image3 from Magic_Science_Lessons where Lesson_ID in {}".format(lesson_id_tuple)
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