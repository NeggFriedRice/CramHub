from flask import Blueprint, jsonify, request
from init import db
from models.threads import Thread, ThreadSchema
from models.comments import Comment, CommentSchema
from models.users import User, UserSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import authorise

threads = Blueprint('threads', __name__, url_prefix='/threads')

# Get all threads
@threads.route("/", methods=["GET"])
def get_all_threads():
    stmt = db.select(Thread)
    threads_list = db.session.scalars(stmt)
    result = ThreadSchema(many=True, exclude=["comments"]).dump(threads_list)
    return jsonify(result)

# Get a single thread
@threads.route("/<int:id>")
def get_a_thread(id):
    stmt = db.select(Thread).where(Thread.id == id)
    thread = db.session.scalar(stmt)
    if not thread:
        return {"CramHub Message": "Thread not found! 😯"}, 404

    result = ThreadSchema().dump(thread)
    return jsonify(result)

# Create new thread
@threads.route("/", methods=["POST"])
@jwt_required()
def create_thread():
    request.json["category"] = request.json["category"].upper()
    thread_fields = ThreadSchema(exclude=['id', 'date']).load(request.json)
    # Get user id from JWT
    user_id = get_jwt_identity()
    new_thread = Thread()
    new_thread.category = request.json["category"]
    new_thread.title = thread_fields["title"]
    new_thread.date = date.today()
    new_thread.description = thread_fields["description"]
    new_thread.link = thread_fields["link"]
    new_thread.user_id = user_id

    db.session.add(new_thread)
    db.session.commit()
    return jsonify(
        ThreadSchema(exclude=["user", "comments"]).dump(new_thread),
        {"CramHub Message": "Thread submitted! 🙂"}), 201

# Update existing thread
@threads.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_thread(id):
    thread_info = ThreadSchema(exclude=['id', 'date']).load(request.json)
    stmt = db.select(Thread).filter_by(id=id)
    thread = db.session.scalar(stmt)

    if not thread:
        return {"CramHub Message": "Thread not found! 😯"}, 404

    thread.category = thread_info.get('category', thread.category)
    thread.title = thread_info.get('title', thread.title)
    thread.description = thread_info.get('description', thread.description)
    thread.link = thread_info.get('link', thread.link)
    db.session.commit()
    return jsonify(
        ThreadSchema().dump(thread),
        {"CramHub Message": f"Thread '{thread.title}' has been updated! 🙂"})

# Delete existing thread
@threads.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_thread(id):
    stmt = db.select(Thread).filter_by(id=id)
    thread = db.session.scalar(stmt)
    if thread:
        authorise(thread.user_id)
        db.session.delete(thread)
        db.session.commit()
    else:
        return {"CramHub Message": "Thread not found! 😯"}, 404
    
    return jsonify(
        {"CramHub Message": "Thread deleted 🙂"})


# Create new comment on thread
@threads.route("/<int:thread_id>/comments", methods=["POST"])
@jwt_required()
def create_comment_on_thread(thread_id):
    # Get fields from the request
    user_id = get_jwt_identity()
    comment_fields = CommentSchema(exclude=['id', 'date']).load(request.json)
    new_comment = Comment()
    new_comment.rating = comment_fields["rating"]
    new_comment.review = comment_fields["review"]
    new_comment.user_id = user_id
    new_comment.thread_id = thread_id
    new_comment.date = date.today()

    db.session.add(new_comment)
    db.session.commit()
    return jsonify(
        CommentSchema().dump(new_comment),
        {" CramHub Message": "Comment submitted! 🙂"}), 201

# Get threads by category
@threads.route('/category/<category>')
def get_threads_by_category(category):
    category = category.upper()
    stmt = db.select(Thread).filter_by(category=category)
    threads = db.session.scalars(stmt)    
    result = ThreadSchema(many=True).dump(threads)
    return jsonify (result)

