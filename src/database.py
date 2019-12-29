import sqlite3 as lite
import csv
import re
import pandas as pd
import hashlib 
from databaseProperties import *


def get_all_students(): 
    con = lite.connect(db)
    cur = con.cursor()
    
    sql='''SELECT * from Students'''
    cur.execute(sql, )
    all_rows=cur.fetchall()
    count=0
    for rows in all_rows: 
        print(rows)
        all_rows[count]=list(rows)
        count=count+1
    return all_rows
def get_all_professors(): 
    con = lite.connect(db)
    cur = con.cursor()
    
    sql='''SELECT * from Professors'''
    cur.execute(sql, )
    all_rows=cur.fetchall()
    count=0
    for rows in all_rows: 
        print(rows)
        all_rows[count]=list(rows)
        count=count+1
    return all_rows
def get_all_courses(): 
    con = lite.connect(db)
    cur = con.cursor()
    
    sql='''SELECT * from Course_taken'''
    cur.execute(sql, )
    all_rows=cur.fetchall()
    count=0
    for rows in all_rows: 
        print(rows)
        all_rows[count]=list(rows)
        count=count+1
    return all_rows
def get_all_classrooms(): 
    con = lite.connect(db)
    cur = con.cursor()
    
    sql='''SELECT * from Classrooms'''
    cur.execute(sql, )
    all_rows=cur.fetchall()
    count=0
    for rows in all_rows: 
        print(rows)
        all_rows[count]=list(rows)
        count=count+1
    return all_rows

def delete_student(data):
    con = lite.connect(db)
    cur = con.cursor()
    parameter = (data[0],)
    sql='''DELETE from Students where sid=(?)'''
    cur.execute(sql, parameter)
    con.commit()
    return True

def delete_professor(data):
    con = lite.connect(db)
    cur = con.cursor()
    parameter = (data[0],)
    sql='''DELETE from Professors where pid=(?)'''
    cur.execute(sql, parameter)
    con.commit()
    return True
    
def delete_classroom(data): 
    con = lite.connect(db)
    cur = con.cursor()
    parameter = (data[0],)
    sql='''DELETE from Classrooms where classroom_id=(?)'''
    cur.execute(sql, parameter)
    con.commit()
    
    parameter = (data[0],)
    sql='''DELETE from Course_taken where classroom_id=(?)'''
    cur.execute(sql, parameter)
    con.commit()
    
    parameter = (data[0],)
    sql='''DELETE from Seats where classroom_id=(?)'''
    cur.execute(sql, parameter)
    con.commit()
    
    return True
#parameter: userType(either 'PROFESSOR' or 'STUDENT') and username
#returns hash string (not a list or tuple)
#if the username is wrong, return None
def get_hash(userType, username): 
    con = lite.connect(db)
    cur = con.cursor()

    if userType == 'PROFESSOR':
        sql = '''
        SELECT p_password_hash FROM Professors
        WHERE ? = p_username
        '''
        
    elif userType == 'STUDENT':
        sql = '''
        SELECT s_password_hash FROM Students
        WHERE ? = s_username
        '''
    else:
        return None

    parameter = (username,)
    cur.execute(sql, parameter)
    result = cur.fetchall()
    if len(result)==0:
        print('Username does not exist!')
        return None
    return result[0][0]

#returns Ture if the user is successfully created
#False if the creation fails		
def create_user(userType, lname, fname, username, password_hash, email): 
    con = lite.connect(db)
    cur = con.cursor()
    if userType == 'PROFESSOR':
        sql_get_id = '''
        SELECT MAX(pid) FROM Professors
        '''
        sql_insert_user = '''
        INSERT INTO Professors VALUES (?,?,?,?,?,?)
        '''
        
    elif userType == 'STUDENT':
        sql_get_id = '''
        SELECT MAX(sid) FROM Students
        '''
        sql_insert_user = '''
        INSERT INTO Students VALUES (?,?,?,?,?,?)
        '''
        
    else:
        return False


    cur.execute(sql_get_id)
    maxID = cur.fetchall()[0][0]
    #print(maxID) #for debug
    newID = 1
    if maxID != None:
        newID = newID+maxID
        
    data = (newID, lname, fname, username, password_hash, email)
        
        
    try:
        cur.execute(sql_insert_user, data)
        con.commit()
    except lite.Error:
        return False
    return True

def hashPassword(password):
    pwHash = password.encode('utf-8')
    return hashlib.sha224(pwHash).hexdigest()

def acceptClassroom(classroomID, sid): 
    con = lite.connect(db)
    cur = con.cursor()
    sql = '''
    UPDATE Course_taken 
    SET status='ACCEPT'
    WHERE classroom_id=(?) AND sid=(?)
    '''
    data=(classroomID, sid)
    cur.execute(sql, data)
    con.commit()
    return True
#p_username: not the pid!
#course_number: e.g. 'ECON 1100'
#course_title: e.g. 'Intermediate Microeconomics'
#returns True if the creation successes
#False if fails
def add_classroom(p_username, classroom_name, dimensionX, dimensionY, course_number, course_title, table):
    con = lite.connect(db)
    cur = con.cursor()
    sql_get_classroom_id = '''
    SELECT MAX(classroom_id) FROM Classrooms
    '''
    cur.execute(sql_get_classroom_id)
    maxID = cur.fetchall()[0][0]
    print(maxID)
    newID = 1
    if maxID != None:
        newID = newID+maxID
    
    
    sql_insert = '''
    INSERT INTO Classrooms VALUES(?,?,?,?,?,?,?)
    '''
    pid = get_id('PROFESSOR',p_username)
    data = (newID, pid, classroom_name, dimensionX, dimensionY, course_number, course_title)
    try:
        cur.execute(sql_insert, data)
        con.commit()
    except lite.Error:
        return False
    rows = len(table)    # 3 rows in your example
    cols = len(table[0]) # 2 columns in your example
    for x in range(rows):
        for y in range(cols):
            #if table[x][y]== "none": 
            #    continue 
            #else:
            data = (newID, x, y, table[x][y], None )
                
            sql = '''
                INSERT INTO Seats VALUES (?,?,?,?,?)
                '''
            cur.execute(sql, data)
            con.commit()
    return True


#the function get_pid(username) has been changed to get_id(userType, username)
#userType: either 'STUDENT' or 'PROFESSOR'
#returns the id (INT), not tuple or list
#returns None if username does not exist
def get_id(userType, username):
    con = lite.connect(db)
    cur = con.cursor()
    
    if userType == 'STUDENT':
        sql = '''
        SELECT sid FROM Students
        WHERE ? = s_username
        '''
        
    elif userType == 'PROFESSOR':
        sql = '''
        SELECT pid FROM Professors
        WHERE ? = p_username
        '''
        
    else:
        return None
    
    parameter = (username,)
    cur.execute(sql, parameter)
    result = cur.fetchall()
    if len(result)==0:
        print('Username does not exist!')
        return None
    return result[0][0]

#students holds array of students
def addCourse(students, classroomID):
    con = lite.connect(db)
    cur = con.cursor()
    
    flag=True
    #fix so that if the get_sid returns null we skip trying to insert 
    #fix get_sid to return the appropriate value 
    for student in students: 
        data=(classroomID, get_sid(student), None, 'INVITE')
        sql = '''
            INSERT INTO Course_taken VALUES (?,?,?,?)
            '''
        try:
            cur.execute(sql, data)
            con.commit()
        except:
            flag=False
            
    
    
    sql='''SELECT * FROM Course_taken'''
    cur.execute(sql)
    all_rows=cur.fetchall()
    print(all_rows)
    
    if flag!=True:
        return False
        
    return True
    #EVENTUALLY WE WANT TO FUNCTION TO RETURN THE NUMBER OF 
    #SUCCESSFUL INVITATIONS
        
def get_sid(email):
    con = lite.connect(db)
    cur = con.cursor()
        
    sql = '''
    SELECT sid FROM Students
    WHERE ? = s_email
    '''
    parameter = (email,)
    cur.execute(sql, parameter)
    result = cur.fetchall()
    if len(result)==0:
        print('Email does not exist!')
        return None
    return result[0][0]

def recallClassroom(classroom_id): 
    con = lite.connect(db)
    cur = con.cursor()

    data = (classroom_id,)
    sql = '''
    SELECT * from Seats where classroom_id=(?)
    '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()
    
    count=0
    for rows in all_rows: 
        all_rows[count]=list(rows)
        count=count+1

    print(all_rows)

    return all_rows
    
def recallStudentClassroom(classroom_id, student_id):
    
    con = lite.connect(db)
    cur = con.cursor()

    data = (classroom_id,)
    sql = '''
    SELECT * from Seats where classroom_id=(?)
        '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()
        
    count=0
    for rows in all_rows: 
        all_rows[count]=list(rows)
        
        if all_rows[count][4] == student_id:
            print("student id matched")
            all_rows[count][3] = 'x'
        count=count+1
    print(all_rows)

    return all_rows
    
def recallAllClassroomInfo(classroom_id, student_id):
    
    con = lite.connect(db)
    cur = con.cursor()

    data = (classroom_id,)
    sql = '''
    SELECT * from Seats seat left outer join Students student on seat.sid=student.sid where classroom_id=(?)
        '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()
    print(all_rows)
    print(len(all_rows))
    count=0
    for rows in all_rows: 
        all_rows[count]=list(rows)
        
        if all_rows[count][4] == student_id:
            print("student id matched")
            all_rows[count][3] = 'x'
        count=count+1
    print(all_rows)

    return all_rows
    
def updateNotes(newNotes):
    con = lite.connect(db)
    cur = con.cursor()
    
    for items in newNotes: 
        data=(items[11], items[0], items[4])
        sql='''
        UPDATE Course_taken
        SET notes=(?) WHERE classroom_id=(?) AND sid=(?)'''
        cur.execute(sql, data)
        con.commit()
    
    sql = '''
    SELECT * from Course_taken
    '''
    cur.execute(sql, )
    print(cur.fetchall())

def getNotes(classroom_id): 
    con = lite.connect(db)
    cur = con.cursor()
    
    data=(classroom_id)
    sql = '''
        SELECT * from Course_taken where classroom_id=(?)
    '''
    cur.execute(sql, data)
    
    all_rows=cur.fetchall()
    print(all_rows)
    return all_rows

    
def updateClassroom(table, student_id, classroom_id):
    # table = x, y coordinates
    con = lite.connect(db)
    cur = con.cursor()
    
    data = (classroom_id, student_id)
    sql = '''
    SELECT * from Seats WHERE classroom_id=(?) AND sid=(?)
    '''
    cur.execute(sql, data)
    all_rows = cur.fetchall()
    #curX = all_rows[0][1]
    #curY = all_rows[0][2]
    
    #data = (classroom_id, student_id)
    sql = '''
    UPDATE Seats
    SET status='open', sid=null
    WHERE classroom_id=(?) AND sid=(?)
    '''
    cur.execute(sql, data)
    con.commit()
    
    data = (classroom_id, table[0], table[1])
    sql = '''
    SELECT * from Seats WHERE classroom_id=(?) AND X_coordinate=(?) AND Y_coordinate=(?) AND status='open'
    '''
    cur.execute(sql, data)
    all_rows = cur.fetchall()
    if len(all_rows) == 0:
        return False
    else:
        data = (student_id, classroom_id, table[0], table[1])
        sql = '''
        UPDATE Seats
        SET status='reserved', sid=(?)
        WHERE classroom_id=(?) and X_coordinate=(?) and Y_coordinate=(?) and status='open'
        '''
        cur.execute(sql, data)
        con.commit()
        return True
        
    
def getDimensions(classroom_id):
    con = lite.connect(db)
    cur = con.cursor()

    data = (classroom_id,)
    sql = '''
    SELECT dimensionX, dimensionY from Classrooms where classroom_id=(?)
    '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()
    dimension=[all_rows[0][0], all_rows[0][1]]
    return dimension

def getAllClassroomData(id): 
    con = lite.connect(db)
    cur = con.cursor()

    data = (id,)
    sql = '''
    SELECT course_title, classroom_name, classroom_id from Classrooms where pid=(?)
    '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()

    user={"classrooms":[]}

    count=0
    for rows in all_rows: 
        user["classrooms"].append({"course": all_rows[count][0], "name": all_rows[count][1], "classroomID":all_rows[count][2]})
        all_rows[count]=list(rows)
        count=count+1

    return user

def recallStudentCourses(id):
    con = lite.connect(db)
    cur = con.cursor()

    data = (id,)
    sql = '''
    SELECT c.course_title, c.classroom_name, c.classroom_id, ct.status 
           from Course_taken ct inner join Classrooms c on c.classroom_id=ct.classroom_id
           where sid=(?)
    '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()

    user={"classrooms":[], "invitations": []}
    
    count=0
    for rows in all_rows: 
        if(all_rows[count][3]=="ACCEPT"):
            user["classrooms"].append({"course": all_rows[count][0], "name": all_rows[count][1], "classroomID":all_rows[count][2], "status": all_rows[count][3]})
            all_rows[count]=list(rows)
            count=count+1
        else:
            user["invitations"].append({"course": all_rows[count][0], "name": all_rows[count][1], "classroomID":all_rows[count][2], "status": all_rows[count][3]})
            count=count+1
    return user
    
def getClassroomTitles(id): 
    con = lite.connect(db)
    cur = con.cursor()

    data = (id,)
    sql = '''
    SELECT course_title, classroom_name from Classrooms where classroom_id=(?)
    '''
    cur.execute(sql, data)
    all_rows=cur.fetchall()
    return all_rows[0]
    
#print(getClassroomTitles(2))    

def updateClassroomLayout(layout, classroom_id):
    
    con = lite.connect(db)
    cur = con.cursor()
    
    data = (classroom_id,)
    sql = '''
    SELECT * from Seats where classroom_id=(?)
    '''
    
    print("printing layout....")
    print(layout)
    cur.execute(sql, data)
    print("we got here")
    all_rows = cur.fetchall()
    
    print("printing all_rows...")
    print(all_rows)
    curr = 0
    for row in all_rows:
        xcor = row[1]
        ycor = row[2]
        if row[3] != layout[xcor][ycor]:
            
            data = (layout[xcor][ycor], classroom_id, xcor, ycor)
            sql = '''
            UPDATE Seats
            SET status=(?), sid=null
            WHERE classroom_id=(?) AND X_coordinate=(?) AND Y_coordinate=(?)
            '''
            cur.execute(sql, data)
            con.commit()
            
        curr = curr + 1
    return True
            
def getRoster(classroom_id):
    con = lite.connect(db)
    cur = con.cursor()
    
    data = (classroom_id,)
    sql = '''
    SELECT s.sid, s.fname, s.lname, s.s_username, s.s_email, ct.status from Course_taken ct inner join Students s on s.sid=ct.sid where classroom_id=(?)
    '''
    
    cur.execute(sql, data)
    all_rows = cur.fetchall()
    return all_rows
    

    