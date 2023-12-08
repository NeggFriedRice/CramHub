from flask import Blueprint, jsonify, request, abort
from init import db
from models.comments import Comment, CommentSchema
from models.users import User, UserSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

comments = Blueprint('comments', __name__, url_prefix='/comments')

@comments.route("/", methods=["GET"])
def get_all_comments():
    stmt = db.select(Comment)
    comments_list = db.session.scalars(stmt)
    result = CommentSchema(many=True).dump(comments_list)

    return jsonify(result)

# Update existing comment
@comments.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_comment(id):

    comment_info = CommentSchema(exclude=['date']).load(request.json)
    stmt = db.select(Comment).filter_by(id=id)
    comment = db.session.scalar(stmt)
    if comment:
        comment.rating = comment_info.get('rating', comment.rating)
        comment.review = comment_info.get('review', comment.review)
        db.session.commit()
        return jsonify(
            CommentSchema().dump(comment),
            {"CramHub Message": f"Comment with ID: '{comment.id}' has been updated! 🙂"})
    else:
        return {'CramHub Message': 'Comment not found'}, 404

# Delete existing comment
@comments.route('/<int:id>', methods=['DELETE'])
def delete_comment(id):
    stmt = db.select(Comment).filter_by(id=id)
    comment = db.session.scalar(stmt)

    if not comment:
        return {"CramHub Message": "Comment not found! 😯"}

    db.session.delete(comment)
    db.session.commit()
    return jsonify(
        CommentSchema().dump(comment),
        {"CramHub Message": f"Comment with ID: '{comment.id}' deleted! 🙂"})