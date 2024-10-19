from App.models import Review, Student
from App.database import db

def create_review(text, student_id, user_id):
    student = Student.query.filter_by(public_id=student_id).first()
    if student:
        review = Review(text, student.id, user_id)
        db.session.add(review)
        db.session.commit()
        return review
    return False