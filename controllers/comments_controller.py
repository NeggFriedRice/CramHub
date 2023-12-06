from flask import Blueprint, jsonify, request, abort
from main import db
from models.comments import Comment
from schemas.comment_schema import comment_schema, comments_schema

comments = Blueprint('comments', __name__, url_prefix='/comments')

@comments.route("/", methods=["GET"])
def get_comments():
    stmt = db.select(Comment)
    comments_list = db.session.scalars(stmt)
    result = comments_schema.dump(comments_list)

    return jsonify(result)
