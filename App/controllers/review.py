from App.models import Review, Student
from App.database import db

def create_review(text, student_id):
    student = Student.query.get(student_id)
    if student:
        review = Review(text, student_id)
        db.session.add(review)
        db.session.commit()
        return review
    return False