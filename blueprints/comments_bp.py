from blueprints.auth_bp import authorise
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.comments import Comment, CommentSchema


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
    # Parse and validate incoming JSON request body through CommentSchema
    comment_info = CommentSchema(exclude=['date']).load(request.json)
    # Select comment from db that matches the passed in id
    stmt = db.select(Comment).filter_by(id=id)
    # Return selected comment
    comment = db.session.scalar(stmt)
    if comment:
        # If comment exists, authorise user
        authorise(comment.user_id)
        # Update comment attributes with incoming JSON body attributes
        comment.rating = comment_info.get('rating', comment.rating)
        comment.review = comment_info.get('review', comment.review)
        # Commit updates
        db.session.commit()
        # Display updated JSONIfied comment and successful update comment to user
        return jsonify(
            CommentSchema(exclude=["user"]).dump(comment),
            {"Message": f"Comment with ID: '{comment.id}' has been updated! 🙂"})
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
    return {"Message": f"Comment with ID '{comment.id}' deleted 🙂"}
