import sqlite3
import random
import configparser
from tkinter import StringVar
TEST_ROW = 16

config = configparser.RawConfigParser()
config.read('magic.cfg')
db = config.get("section1",'dataroot')
imageroot = config.get("section1",'image_root')
videoroot = config.get("section1",'video_root')

def get_Images(lesson_id_list):

    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Factual_Image1,Factual_Image2,Factual_Image3 from Magic_Science_Lessons where Lesson_ID in (?)"
    cur.execute(sql, (lesson_id_list, ))
    images = cur.fetchone()
    connection.commit()
    connection.close()
    return images

def get_Fact_Terms(lesson_id_list):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    lesson_id_tuple = tuple(lesson_id_list)
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
    sql = "select Factual_Term1_Description, Factual_Term2_Description, Factual_Term3_Description from Magic_Science_Lessons where Lesson_ID in ?"
    cur.execute(sql, (lesson_id_list,))
    descriptions = cur.fetchone()
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