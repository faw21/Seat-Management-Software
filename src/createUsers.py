from database import *


create_user("PROFESSOR", "Tim", "Teacher", "teacher", hashPassword("p") , 'teacher@pitt.edu')
create_user("STUDENT", "Jordan", "Connor", "CAJ", hashPassword("p") , 'caj@pitt.edu')
create_user("STUDENT", "Beck", "Randall", "RAB", hashPassword("p") , 'rab@pitt.edu')
create_user("STUDENT", "Han", "Jerry", "JH", hashPassword("p") , 'jh@pitt.edu')
create_user("STUDENT", "Lin", "Jared", "JL", hashPassword("p") , 'jl@pitt.edu')
create_user("STUDENT", "Wu", "Aaron", "AW", hashPassword("p") , 'aw@pitt.edu')
create_user("STUDENT", "Smith", "John", "JS", hashPassword("p") , 's1@pitt.edu')
create_user("STUDENT", "Jones", "Jay", "JJ", hashPassword("p") , 's2@pitt.edu')
create_user("STUDENT", "Wu", "Jimmy", "JW", hashPassword("p") , 's3@pitt.edu')

