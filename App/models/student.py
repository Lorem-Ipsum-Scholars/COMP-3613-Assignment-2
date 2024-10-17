from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique = True, nullable = False)
    firstname =  db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    reviews = db.relationship('Review', backref = 'student', lazy = True, cascade="all, delete-orphan")
    email = db.Column(db.String(100), nullable = False, unique = True)

    def __init__(self, firstname, lastname, email, public_id):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.public_id = public_id
    
    def to_json(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'reviews': [review.to_json() for review in self.reviews] if self.reviews else []
        }
