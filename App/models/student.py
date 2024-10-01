from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname =  db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    reviews = db.relationship('Review', backref = 'student', lazy = True, cascade="all, delete-orphan")

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    
    def to_json(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'reviews': [review.to_json() for review in self.reviews] if self.reviews else []
        }
    def __repr__(self):
        return f"id:{self.id} Name:{self.firstname} {self.lastname}"
