from .user import create_user
from .student import create_student
from .review import create_review
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    #bob = create_user('bob', 'bobpass', 'bob@mail.com')
