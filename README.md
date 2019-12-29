# Seat Pursuit
Project from software engineering class

#### INSTRUCTIONS

#### To run: 
1) You may need to use command "pip3 install flask" in terminal to install the backend application <br>
2) Make any back end edits in main.py <br>
3) BE SURE TO PIP INSTALL ALL THE IMPORT STATEMENTS AT THE TOP OF MAIN.PY 
4) To run the app, cd into the source code folder and run python3 main.py on the terminal <br>
5) If the app runs correctly, you will see Running on: "http://....." after the script starts<br>
6) Copy the http:// link into your browser to view the website <br>
7) You can continue to edit html files while the script is running. Refresh your browser to view changes.  <br>

#### DOCUMENTATION 
###### (10/27/19)
	Uploaded the file structure for a Python web app. 
###### (10/28/19) 
	Created user login front end/ login data is received in backend. Isn't connected to the database yet.
	Created sessions. Persists between pages while user is logged in 
	Created logout function. Logs user out and returns them to home page
	Logout doesn't occur at browser closed. 
	Created class for Account Creation 
	Created Account Creation Page
###### (10/29/19)
	Created classroom edit page
	Updated user creation page
	Updated classroom creation page
	
###### (10/29/19) 
	Created Home Page interface

##### (10/30/19) 
	Added Classroom Preview to the Classroom Creator (i.e you can see what the classroom will look like
	when you enter classroom editor. 
	BUG NEEDING ADDRESSED: Sometimes, grid squares will spill over into the next row for grid width-20 when you
	resize browser.
	
##### (10/31/19)
	Added basic Classroom Editor. 
	~~BUG NEEDING ADDRESSED: AJAX doesn't deliver array on seat status's properly ~~
	~~BUG NEEDING ADDRESSED: Sometimes, grid squares will spill over into the next row for grid width-20 when you
	resize browser (Classroom Creator)~~ 

##### (11/2/19). 
	Added fully functioning Classroom Editor.  
	Login Validation is Functional. 
	Created database.py to hold all functions involving database queries 
	BUG FIXED: AJAX doesn't deliver array on seat status's properly
	BUG FIXED: Sometimes, grid squares will spill over into the next row for grid width-20 when you
	resize browser (Classroom Creator) 

##### (11/3/19) 
	Created reset.py. This clears the database so if something goes horribly wrong, we can restart filling with test accounts.
	Professors can now edit classrooms. 
	Professors dashboard includes all of their classes that are in the database. 
	BUG NEEDING ADDRESSED: login doesn't catch invalid users correctly. need to show debugging error 
