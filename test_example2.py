import json
from queue import Empty
import pytest
import System
import Staff
import User


username = 'calyam'
password =  '#yeet'
username2 = 'hdjsr7'
username3 = 'yted91'
course = 'cloud_computing'
assignment = 'assignment1'
profUser = 'goggins'
profPass = 'augurrox'

#Tests if the program can handle a wrong username
grade = 200
grades = []
assign = []

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem

#doesn't work because username doesn't exist
def test_login(grading_system):
    grading_system.login(username,password)
    i = 0
    while i != 1:
        if grading_system.users[username]['courses'][i] == course:
            assert True
        i = i + 1
    

def test_check_password(grading_system):
    test = grading_system.check_password(username,password)
    test2 = grading_system.check_password(username,'#YEET')
    if test == test2:
        assert False
    else: 
        assert True
    

#doesn't work due to the fact that the change grade function always changes the grade to zero
def test_change_grade(grading_system):
    grading_system.login(username, password)
    grading_system.usr.change_grade(username3,course,assignment,grade)
    grades = grading_system.users[username3]['courses'][course][assignment]['grade']
    if grades == grade:
        assert True
    else:
        assert False
    
#doesn't work for any course but comp_sci 
def test_create_assignment(grading_system):
    grading_system.login(username, password)
    grading_system.usr.create_assignment('assignment20','09/12/22',course)
    grading_system.login(username3,'imoutofpasswordnames')
    assign = grading_system.users[username3]['courses'][course]
    d = 1
    for x in assign:
        if 'assignment20' in x:
            d = 0
            return True
    if d == 1:
        return False  

#doesn't work because list indices must be integers
def test_add_student(grading_system):
    grading_system.login(username,password)
    grading_system.usr.add_student('akend3',course)
    grading_system.login('akend3','123454321')
    assign = grading_system.usr.view_assignments(course)
    if assign != []:
        assert True
    else:
        assert False

def test_drop_student(grading_system):
    grading_system.login(username,password)
    grading_system.usr.drop_student(username3,course)
    courses = grading_system.users[username3]['courses']
    d = 1
    for xx in courses:
        if(xx != course):
            d = 0
            assert True
    if d == 1:
        assert False

def test_submit_assignment(grading_system):
    grading_system.login(username3,'imoutofpasswordnames')
    grading_system.usr.submit_assignment('software_engineering',assignment,'Nothing to see here','10/9/22')
    submission = grading_system.users[username3]['courses']['software_engineering'][assignment]['submission']
    d = 1
    if(submission == 'Nothing to see here'):
        assert True
    else:
        assert False

#doesn't work for cloud_computing due to second assignment dict name being Submission Data
def test_check_onTime(grading_system):
    time = grading_system.users[username3]['courses'][course]
    due = grading_system.courses[course]['assignments']
    d = 1
    for sub in time:
        if time[sub]['submission_date'] == due[sub]['due_date']:
            d = 0
            assert True
        else:
            d = 1
    if d == 1:
        assert False

#doesn't work for cloud_computing due to key error
def test_check_grades(grading_system):
    grading_system.login(username3,'imoutofpasswordnames')
    check = grading_system.usr.check_grades(course)
    grad = grading_system.users[username3]['courses'][course]
    d = 0
    for sub in grad:
        if grad[sub]['grade'] == check[d][1]:
            assert True
        else:
            assert False
        d = d + 1

def test_view_assingments(grading_system):       
    grading_system.login(username3,'imoutofpasswordnames')
    check = grading_system.usr.view_assignments(course)
    check2 = grading_system.users[username3]['courses'][course]
    d = 0
    for sub in check2:
        if sub == check[d] and check2[sub]['due_date'] == check[d]:
            assert True
        else:
            assert False
        d = d + 1
    
def test_add_student_to_not_taught_course(grading_system):
    grading_system.login(profUser,profPass)
    grading_system.usr.add_student('akend3',course)
    grading_system.login('akend3','123454321')
    assign = grading_system.usr.view_assignments(course)
    if assign != []:
        assert True
    else:
        assert False

def test_drop_student_from_not_taught_course(grading_system):
    grading_system.login(profUser,profPass)
    grading_system.usr.drop_student(username3,course)
    courses = grading_system.users[username3]['courses']
    d = 1
    for xx in courses:
        if(xx != course):
            d = 0
            assert False
    if d == 1:
        assert True

def test_login_with_different_case_username(grading_system):
    username = 'CALYAM'
    password =  '#yeet'
    grading_system.login(username,password)

def test_if_create_assignment_for_course_not_taught(grading_system):
    grading_system.login(profUser, profPass)
    grading_system.usr.create_assignment('assignment30','09/12/22',course)
    grading_system.login(username3,'imoutofpasswordnames')
    assign = grading_system.usr.view_assignments(course)
    d = 1
    for x in assign:
        if 'assignment30' in x:
            d = 0
            assert True
    if d == 1:
        assert False 

def test_if_can_submit_assignment_for_course_not_in(grading_system):
    grading_system.login('akend3','123454321')
    grading_system.usr.submit_assignment(course,assignment,'Nothing to see here','10/9/22')
    submission = grading_system.users['akend3']['courses'][course][assignment]['submission']
    d = 1
    if(submission == 'Nothing to see here'):
        assert True
    else:
        assert False