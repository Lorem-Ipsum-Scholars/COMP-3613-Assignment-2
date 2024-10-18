from flask import Blueprint, jsonify, request
from App.controllers.review import create_review
from flask_jwt_extended import jwt_required

review_views = Blueprint('review_views', __name__)

@review_views.route('/reviews', methods=['POST'])
@jwt_required()
def create_review_view():
    data = request.json
    text = data.get('text')
    student_id = data.get('student_id')
    user_id = data.get('user_id')
    
    if not text or not student_id or not user_id:
        return jsonify({"error": "Missing text or student_id"}), 400
    
    review = create_review(text, student_id, user_id)
    if review:
        return jsonify(review.to_json()), 201
    return jsonify({"error": "Student not found"}), 404