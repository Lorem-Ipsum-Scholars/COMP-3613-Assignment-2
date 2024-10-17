import os, tempfile, pytest, logging, unittest

import unittest.test
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Review
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("jane", "smith", "jane.smith@mail.com", 816012345)
        assert student.firstname == "jane" and student.lastname == "smith" and student.email == "jane.smith@mail.com" and student.public_id == 816012345

    def test_to_json(self):
        student = Student("jane", "smith", "jane.smith@mail.com", 816012345)
        student_json = student.to_json()
        self.assertDictEqual(student_json, {"id": None, "public_id": 816012345, "firstname": "jane", "lastname": "smith", "email":"jane.smith@mail.com", "reviews": []})

class ReviewUnitTests(unittest.TestCase):
    def test_new_review(self):
        review = Review("Test Review", 1, 1)
        assert review.text == "Test Review" and review.student_id == 1 and review.user_id == 1
    
    def test_to_json(self):
        review = Review("Test Review", 1, 1)
        review_json = review.to_json()
        self.assertDictEqual(review_json, {
            'id': None,
            'text': "Test Review",
            'student_id': 1,
            'user_id': 1
        })

class UserUnitTests(unittest.TestCase):

    def test_create_user(self):
        user = User("bob", "bobpass", "bob.smith@mail.com")
        assert user.username == "bob" and user.email == "bob.smith@mail.com"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass", "bob.smith@mail.com")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "email": "bob.smith@mail.com"})
    
    def test_user_set_password(self):
        password = "newpass"
        user = User("bob", "bobpass", "bob@mail.com")
        user.set_password(password)
        print(generate_password_hash(password) + "\n")
        print(user.password)
        assert check_password_hash(user.password, password) 
        self.assertFalse(check_password_hash(user.password, "bobpass"))
                         
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password, "bob.smith@mail.com")
        assert user.password != password

    def test_user_check_password(self):
        password = "bobpass"
        user = User("bob", password, "bob.smith@mail.com")
        self.assertTrue(user.check_password(password))
        self.assertFalse( user.check_password("FAKEpass"))


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass", "bob@mail.com")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "rickpass","rick@mail.com")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        user = create_user("bob", "bobpass", "bob@mail.com")
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"rick", "email":"rick@mail.com"}, {"id":2, "username":"bob", "email":"bob@mail.com"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

