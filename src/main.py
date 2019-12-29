from flask import Flask, render_template, request, json, session, flash, url_for, abort, g, make_response, redirect
import http.client, random
from wtforms import Form, BooleanField, TextAreaField, StringField, validators, SelectField, SubmitField, IntegerField, FileField, RadioField
from flask_wtf import FlaskForm
import  sqlite3 as lite
from flask_wtf.csrf import CSRFProtect
import json
import requests
import simplejson
from database import *
from wtforms.validators import DataRequired
from databaseProperties import *

app = Flask(__name__)
csrf = CSRFProtect(app)
SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'rosters'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])



class LoginInformation(FlaskForm): 
	username = StringField('username', [validators.Length(min=7, max=15)])
	password = StringField('password', [validators.Length(min=7, max=15)])
	user_type = SelectField('user_type',[validators.DataRequired()], choices=[('Professor','Professor'),('Student','Student')])
	submit = SubmitField('Submit')
	
class Edit(FlaskForm):
	edit = SubmitField('Edit')
	
class Admin(FlaskForm): 
	password = StringField('password', [validators.Length(min=7, max=15)])
	submit = SubmitField('Submit')

	
class AccountCreator(FlaskForm): 
	fname = StringField('fname', [validators.DataRequired()])
	lname = StringField('fname', [validators.DataRequired(), validators.Length(min=1, max=50)])
	username = StringField('username', [validators.DataRequired(), validators.Length(min=3, max=50)])
	password = StringField('password', [validators.DataRequired(), validators.Length(min=7, max=15)])
	email = StringField('email', [validators.DataRequired(), validators.Length(min=6, max=200)])
	user_type = SelectField('user_type',[validators.DataRequired()], choices=[('Professor','Professor'),('Student','Student')])
	submit = SubmitField('Submit')

class Roster(FlaskForm):
	email= StringField('email', [validators.Length(min=6, max=200)])
	students = FileField('students')
	submit = SubmitField('Submit')
	
class ClassroomCreator(FlaskForm): 
	classroomName = StringField('classroomName', [validators.DataRequired()])
	course_number = StringField('course_number', [validators.DataRequired()])
	course_title = StringField('course_title', [validators.DataRequired()])
	semester = StringField('semester', [validators.DataRequired()])
	dimensionX = SelectField('dimensionX',[validators.DataRequired()], choices=[(5,5),(10,10),(15,15),(20,20),(30,30)])
	dimensionY = SelectField('dimensionY',[validators.DataRequired()], choices=[(5,5),(10,10),(15,15),(20,20),(30,30)])
	submit = SubmitField('Submit')
	
@app.route('/admin', methods = ['GET','POST'])
def admin():
	form=Admin()
	if form.validate and request.method == 'POST':
		if form.password.data=="password":
			#print(get_all())
			return render_template('admin.html', students=get_all_students(), professors=get_all_professors(), classrooms=get_all_classrooms())
		
	return render_template('a_log.html', form=form)
	
@csrf.exempt 
@app.route('/createDatabaseStudent', methods=['GET', 'POST'])
def createDatabaseStudent():
	print("called function....")
	if request.method == "POST":
		grid=json.loads(request.data)
		create_user("STUDENT", grid['lname'], grid['fname'], grid['username'], hashPassword(grid['password']), grid['email'])
		return "okay"
@csrf.exempt 
@app.route('/createDatabaseProfessor', methods=['GET', 'POST'])
def createDatabaseProfessor():
	print("called function....")
	if request.method == "POST":
		grid=json.loads(request.data)
		create_user("PROFESSOR", grid['lname'], grid['fname'], grid['username'], hashPassword(grid['password']), grid['email'])
		return "okay"
		
@csrf.exempt 
@app.route('/processDeleteStudent', methods=['GET', 'POST'])
def processDeleteStudent(): 
	print("method called")
	if request.method == "POST":
			grid=json.loads(request.data)
			print("printing student....")
			print(grid['student'])
			delete_student(grid['student'])
			
	return "okay"
	
@csrf.exempt 
@app.route('/processDeleteProfessor', methods=['GET', 'POST'])
def processDeleteProfessor(): 
	if request.method == "POST":
			grid=json.loads(request.data)
			delete_professor(grid['professor'])
	return "okay"
	
@csrf.exempt 
@app.route('/processDeleteClassroom', methods=['GET', 'POST'])
def processDeleteClassroom(): 
	if request.method == "POST":
			grid=json.loads(request.data)
			print("printing classroom....")
			print(grid['classroom'])
			delete_classroom(grid['classroom'])
	return "okay"
	

@csrf.exempt
@app.route('/updateStudentSeat', methods=['GET', 'POST'])
def updateStudentSeat():
	if request.method == "POST":
		grid=json.loads(request.data)
		print(grid)
		updateClassroom([grid["x"], grid["y"]], session['id'], grid["classroomID"])
		return "success"

@app.route('/seatSelect/<classroomID>',  methods=['GET', 'POST'])
def seatSelect(classroomID):
	print("in seat select")
	print(session['classrooms'])
	print(classroomID)
	if int(classroomID) in session['classrooms']:
		print(recallStudentClassroom(classroomID, session['id']))
		classroomData=getClassroomTitles(classroomID)
		
		return render_template('pick.html', x=getDimensions(classroomID)[0], y=getDimensions(classroomID)[1], configuration=json.dumps(recallStudentClassroom(classroomID, session['id'])), classroomID=classroomID, courseTitle=classroomData[0], classroomName=classroomData[1])
	else:
		return redirect('/')
	
@app.route('/accept/<classroomID>', methods=['GET', 'POST'])
def accept(classroomID):
	print(classroomID)
	acceptClassroom(classroomID, session['id'])
	return redirect('/')

@csrf.exempt
@app.route('/validateNotes', methods=['GET', 'POST'])
def validateNotes():
	if request.method == "POST":
			grid=json.loads(request.data)
			data=grid["myArray"]
			print("printing grid data")
			validated=[items for items in data if len(items)>11]
			print(validated)
			updateNotes(validated)
	
	return "okay"
	
@app.route('/view/<classroomID>', methods=['GET', 'POST'])
def view(classroomID):
	classroomData=getClassroomTitles(classroomID)
	
	if session['type']=="PROFESSOR":
			data=recallAllClassroomInfo(classroomID, -1) 
			notes=getNotes(classroomID)
			print("printing notes....")
			print(notes)
			for note in notes: 
				for items in data: 
					if note[1]!=None:
						if note[1]==items[4]: 
							if note[2]!=None:
								items.append(note[2])
						
			return render_template('addNotes.html', x=getDimensions(classroomID)[0], y=getDimensions(classroomID)[1], configuration=json.dumps(data), classroomID=classroomID, courseTitle=classroomData[0], classroomName=classroomData[1])
	elif session['type']=="STUDENT":
		return render_template('view.html', x=getDimensions(classroomID)[0], y=getDimensions(classroomID)[1], configuration=json.dumps(recallAllClassroomInfo(classroomID, session['id'])), classroomID=classroomID, courseTitle=classroomData[0], classroomName=classroomData[1])
	else:
		return redirect('/')
		
	
@csrf.exempt
@app.route('/classroomUpdateValidation', methods=['GET', 'POST'])
def classroomUpdateValidation():
	if request.method == "POST":
		grid=json.loads(request.data)
		table=[]
		userInput=grid["myArray"]
		
		element=0
		for y in range (grid["y"]): 
			table.append([])
			for x in range (grid["x"]): 
				print(userInput[element])
				table[y].append(userInput[element])
				element=element+1
		
		updateClassroomLayout(table, grid["classroomID"])
		return "success"
	return "failure"

@app.route('/viewRoster/<classroomID>',  methods=['GET', 'POST'])
def viewRoster(classroomID): 
		return render_template('viewRoster.html', students=getRoster(classroomID), attributes=getClassroomTitles(classroomID))
	
	
@app.route('/editor/<classroomID>',  methods=['GET', 'POST'])
def editor(classroomID): 
	print(classroomID)
	classroomData=getClassroomTitles(classroomID)
	return render_template('editor.html', x=getDimensions(classroomID)[0], y=getDimensions(classroomID)[1], configuration=json.dumps(recallClassroom(classroomID)), classroomID=classroomID, courseTitle=classroomData[0], classroomName=classroomData[1] )
	
@app.route('/rosterCreator', methods=['GET', 'POST'])
def rosterCreator(classroomID):
	print(classroomID)
	form=Roster()
	if form.validate and request.method == 'POST':
		print(form.students.data)
		try:
			file_data = form.students.data.read().decode('utf-8') #csv file data
		except:
			return redirect('/error')
			
		arrStudent = file_data.split(',')
		for i in range(len(arrStudent)): 
			arrStudent[i]=arrStudent[i].replace(" ", "")
			arrStudent[i]=arrStudent[i].replace("\n", "")
		
		success=addCourse(arrStudent, classroomID)
		if success!=True:
			return redirect('/error')
		
		return redirect('/')
		
	return render_template('rosterCreator.html',  form=form)

@app.route('/error', methods=['GET', 'POST'])
def error():
	return render_template('error.html')

@app.route('/roster/<classroomID>', methods=['GET', 'POST'])
def roster(classroomID):
	return rosterCreator(classroomID)

@app.route('/help', methods=['GET', 'POST'])
def help():
	return render_template('help.html')
	
@csrf.exempt
@app.route('/gridReceive', methods=['GET', 'POST'])
def gridReceive():
	if request.method == "POST":
		grid=json.loads(request.data)
		table=[]
		userInput=grid["myArray"]
		
		element=0
		for y in range (grid["y"]): 
			table.append([])
			for x in range (grid["x"]): 
				print(userInput[element])
				table[y].append(userInput[element])
				element=element+1
		
		print(table)
		print("length of table "+str(len(table)))
	add_classroom(session['username'], grid["classroomName"], grid["x"], grid["y"], grid["course_number"] , grid["course_title"], table)
	
	#################
	con = lite.connect(db)
	cur = con.cursor()

	cur.execute("SELECT * from Seats")
	all_rows=cur.fetchall()
	print(all_rows)
	print()
	
	cur.execute("SELECT * from Classrooms")
	all_rows=cur.fetchall()
	print(all_rows)
	print()
	
	#grid=json.loads(request.data)
	#print(grid["myArray"][0])
	return 'success'

	
@app.route('/editClassroom', methods = ['GET', 'POST'])
def editClassroom(xDimension, yDimension, classroomName, course_number, course_title):
		return render_template('editClassroom.html', x=xDimension, y=yDimension, classroomName=classroomName, course_number=course_number, course_title=course_title) # finish when we have a design in the HTML

@app.route('/classroomCreator', methods = ['GET','POST'])
def classroomCreator():  
	if 'username' in session:
		form=ClassroomCreator()
		if form.validate and request.method == 'POST':
			classroomName=(form.classroomName.data).split()
			course_number=(form.course_number.data).split()
			course_title=(form.course_title.data).split()
			
			return editClassroom(form.dimensionX.data, form.dimensionY.data, classroomName, course_number, course_title)
						
		if not form.validate:
			print("Not valid")
		return render_template('classroomCreator.html', form=form, invalid="False")
	else:
		return redirect('/')
	
	
@app.route('/logout')
def logout():
	session.pop('username', None) 
	print("logout successful")
	return redirect('/')


@app.route('/',  methods = ['GET','POST'])
def userValidation():
	if 'username' not in session:
		form=LoginInformation()
		if form.validate and request.method == 'POST':
			
			validEntry="STUDENT"
			if form.user_type.data == "Professor":
				validEntry="PROFESSOR"
			
			entered_hash=hashPassword(form.password.data)
			actualHash=get_hash(validEntry, form.username.data)
			print(actualHash)
			if actualHash == entered_hash:
				session['username']=form.username.data
				session['id']=get_id(validEntry, form.username.data)
				session['type']=validEntry
				return redirect('/')
			else:
				return render_template('login.html', form=form, invalid="True")
		if not form.validate:
			print("Not validate")
			return render_template('login.html', form=form, invalid="False")
		return render_template('login.html', form=form, invalid="False")
	else: 
		return redirect('/home')

@app.route('/studentHome', methods= ['GET', 'POST'])
def studentHome():
	if session['type']=="STUDENT":
		user = recallStudentCourses(session['id'])
		session['classrooms']=[]
		for classes in user['classrooms']: 
			session['classrooms'].append(classes['classroomID'])
		print(session['classrooms'])
		print(user)
		return render_template('studentHome.html', user=user)
	else:
		return redirect('/')
@app.route('/home', methods= ['GET', 'POST'])
def home():
	if 'username' in session: 
		if session['type']=="PROFESSOR":
			form=Edit()
			if form.validate and request.method == 'POST':
				print(form.edit.data)
		
			user=getAllClassroomData(session['id'])
			return render_template('home.html', user=user)
		else:
			return redirect('/studentHome')
	
@app.route('/accountCreation', methods = ['GET', 'POST'])
def accountCreation(): 
		form=AccountCreator()
		if form.validate and request.method == 'POST': 
			#validate the account 
			print(form.fname.data)
			print(form.lname.data)
			print(form.username.data)
			print(form.user_type.data)
			print(form.password.data)
			print(hashPassword(form.password.data))
			print(form.email.data)
			#need to check if any fields are null 
			if(form.user_type.data == "Professor"):
				print("sending professor data")
				print(create_user("PROFESSOR", form.lname.data, form.fname.data, form.username.data, hashPassword(form.password.data), form.email.data))
				con = lite.connect(db)
				cur = con.cursor()

				cur.execute("SELECT * from Professors")
				all_rows=cur.fetchall()
				print(all_rows)
				print("all_rows has been printed")
				return redirect('/')
			elif(form.user_type.data == "Student"):
				print(create_user("STUDENT", form.lname.data, form.fname.data, form.username.data, hashPassword(form.password.data), form.email.data))
				con = lite.connect(db)
				cur = con.cursor()

				cur.execute("SELECT * from Students")
				all_rows=cur.fetchall()
				print(all_rows)
				print("all_rows has been printed")
				return redirect('/')
		if not form.validate: 
			print("Not validate")
		
		return render_template('accountCreation.html', form=form, invalid="True")

if __name__ == "__main__":
	app.run(debug=True)
	