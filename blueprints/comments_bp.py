from flask import Blueprint, jsonify, request, abort
from init import db
from models.comments import Comment, CommentSchema
from models.users import User, UserSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import authorise

# Comments blueprint registered in main
comments = Blueprint('comments', __name__, url_prefix='/comments')


# Get all comments
@comments.route("/", methods=["GET"])
def get_all_comments():
    # Selects all comments objects from db
    stmt = db.select(Comment)
    # Returns all selected comments objects
    comments_list = db.session.scalars(stmt)
    # Comments objects parsed through CommentSchema
    result = CommentSchema(many=True).dump(comments_list)
    # Display JSONified result
    return jsonify(result)


# Update existing comment (by comment id)
@comments.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(id):
    # Parses and validates incoming JSON request body through CommentSchema
    comment_info = CommentSchema(exclude=['date']).load(request.json)
    # Selects comment from db that matches the passed in id
    stmt = db.select(Comment).filter_by(id=id)
    # Returns the selected comment
    comment = db.session.scalar(stmt)
    if comment:
        # If comment exists, authorise user
        authorise(comment.user_id)
        # Update comment rating with JSON request 'rating'
        comment.rating = comment_info.get('rating', comment.rating)
        # Update comment review with JSON request 'review'
        comment.review = comment_info.get('review', comment.review)
        # Commit updates
        db.session.commit()
        return jsonify(
            # Display updated JSONIfied successful update comment to user
            CommentSchema(exclude=["user"]).dump(comment),
            {"Error": f"Comment with ID: '{comment.id}' has been updated! 🙂"})
    else:
        # If commenot not found, show error message
        return {'Error': 'Comment not found! 😯'}, 404


# Delete existing comment
@comments.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    # Select comment from db that matches the passed in id
    stmt = db.select(Comment).filter_by(id=id)
    # Returns the selected comment
    comment = db.session.scalar(stmt)
    if comment:
        # If comment exists, authorise user
        authorise(comment.user_id)
        # Delete comment
        db.session.delete(comment)
        # Commit changes
        db.session.commit()
    else:
        # If comment does not exist, show error message
        return {"Error": "Comment not found! 😯"}, 404
    # Display successful delete message to user
    return {"Error": f"Comment with ID '{comment.id}' deleted 🙂"}
