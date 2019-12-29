import sqlite3 as lite
import csv
import re
import pandas as pd
import hashlib 
from databaseProperties import *

con = lite.connect(db)
cur = con.cursor() 

cur.execute('DROP TABLE IF EXISTS Students')
cur.execute("CREATE TABLE Students(sid INT, fname TEXT, lname TEXT, s_username CHAR(16) UNIQUE, s_password_hash TEXT, s_email CHAR(16) UNIQUE, PRIMARY KEY(sid))")

cur.execute('DROP TABLE IF EXISTS Professors')
cur.execute("CREATE TABLE Professors(pid INT, fname TEXT, lname TEXT, p_username CHAR(16) UNIQUE, p_password_hash TEXT, p_email CHAR(16) UNIQUE, PRIMARY KEY(pid))")

cur.execute('DROP TABLE IF EXISTS Course_taken')
cur.execute("CREATE TABLE Course_taken(classroom_id INT, sid INT, notes TEXT, status TEXT, UNIQUE(classroom_id, sid))")

cur.execute('DROP TABLE IF EXISTS Classrooms')
cur.execute("CREATE TABLE Classrooms(classroom_id INT, pid INT, classroom_name TEXT, dimensionX INT, dimensionY INT, course_number char(10), course_title TEXT, PRIMARY KEY(classroom_id), UNIQUE(pid, classroom_name))")
    
cur.execute('DROP TABLE IF EXISTS Seats')
cur.execute("CREATE TABLE Seats(classroom_id INT, X_coordinate INT, Y_coordinate INT, status char(10), sid INT, UNIQUE(classroom_id, X_coordinate, Y_coordinate))")