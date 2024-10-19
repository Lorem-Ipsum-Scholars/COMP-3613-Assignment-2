from flask import Blueprint, jsonify, request
from App.controllers.student import (create_student, search_student, search_student_by_public_id, review_student, view_reviews)
from flask_jwt_extended import jwt_required

student_views = Blueprint('student_views', __name__)

@student_views.route('/students', methods=['POST'])
@jwt_required()
def create_student_view():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    public_id = data.get('public_id')
    
    if not firstname or not lastname or not email or not public_id:
        return jsonify({"error": "Missing firstname , lastname , email or public ID"}), 400
    
    student = create_student(firstname, lastname, email, public_id)
    if student:
        return jsonify(student.to_json()), 201
    return jsonify({"error": "Email/Id already taken"}), 400


@student_views.route('/students/<int:id>', methods=['GET'])
@jwt_required()
def search_student_view(id):
    student = search_student_by_public_id(id)
    if student: 
        return jsonify(student.to_json()), 200
    return jsonify({"error": "Student not found"}), 404


@student_views.route('/students/<int:id>/reviews', methods=['GET'])
@jwt_required()
def view_reviews_view(id):
    reviews = view_reviews(id)
    if reviews:
        return jsonify(reviews), 200
    return jsonify({"error": "No reviews found"}), 404