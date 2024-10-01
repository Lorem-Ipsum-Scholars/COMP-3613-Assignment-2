from App.models import Student
from .review import create_review
from App.database import db

def create_student(firstname, lastname):
    student = Student(firstname, lastname)
    db.session.add(student)
    db.session.commit()
    return student

def search_student(id):
    student = Student.query.get(id)
    return student

def review_student(id, text):
    student = search_student(id)
    if student:
        review = create_review(text, student.id)
        student.reviews.append(review)
        db.session.add(student)
        db.session.commit()
        return review
    return False
    
def view_reviews(id):
    student = search_student(id)
    if student:
        reviews = []
        for review in student.reviews:
            reviews.append(review.to_json())
        return reviews
    return False