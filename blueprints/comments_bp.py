from flask import Blueprint, jsonify, request, abort
from init import db
from models.comments import Comment, CommentSchema
from models.users import User, UserSchema
from datetime import date

comments = Blueprint('comments', __name__, url_prefix='/comments')

@comments.route("/", methods=["GET"])
def get_all_comments():
    stmt = db.select(Comment)
    comments_list = db.session.scalars(stmt)
    result = CommentSchema(many=True).dump(comments_list)

    return jsonify(result)


# Create new comment
@comments.route("/", methods=["POST"])
def create_thread():
    comment_fields = CommentSchema(exclude=['id', 'date']).load(request.json)
    new_comment = Comment()
    new_comment.rating = comment_fields["rating"]
    new_comment.review = comment_fields["review"]
    new_comment.date = date.today()

    db.session.add(new_comment)
    db.session.commit()
    return jsonify(
        CommentSchema().dump(new_comment),
        {" CramHub Message": "Comment submitted!"}), 201

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