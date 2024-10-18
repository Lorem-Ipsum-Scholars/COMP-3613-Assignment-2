import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_student, search_student, review_student, view_reviews)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')




student_cli = AppGroup('student', help='Student Object commands')

@student_cli.command("create", help="Creates a student")
def create_student_command():
    firstName  = input("Enter the first name\n")
    lastName = input("Enter the last name\n")
    email = input("Enter the Email\n")
    student_id = input("Enter the student's id\n")
    print(firstName)
    student = create_student(firstName, lastName, email, student_id)
    print(f"Student {firstName} {lastName} created with ID {student.id}!")

@student_cli.command("search", help="Search for a student")
def search_student_command():
    id = input("Enter the student's ID\n")
    student = search_student(id)
    if student:
        print("Student information in JSON format: ")
        print(student.to_json())
    else:
        print("Student does not exist")

@student_cli.command("review", help="Reviews a student. (Maximum of 500 characters)")
def review_student_command():
    id = input("Enter the student's ID\n")
    text = input("Enter the review's content\n")
    review = review_student(id, text)
    if review:
        print("Review in JSON format: ")
        print(review.to_json())
    else:
        print("Review failed because a student is not associated with that ID.")

@student_cli.command("view_reviews", help="View a student's reviews")
def view_reviews_command():
    id = input("Enter the student's ID\n")
    reviews = view_reviews(id)
    if reviews:
        print("Reviews in JSON format: ")
        print(reviews)
    else:
        print("Student does not exist.")

app.cli.add_command(student_cli)





'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UsersIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentsIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReviewsIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)