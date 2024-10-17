from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable = False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    user_id = db.column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, text, student_id):
        self.text = text
        self.student_id = student_id

    
    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'student_id': self.student_id,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f"id:{self.id} Content:{self.text} Student ID:{self.student_id} User ID:{self.user_id}"