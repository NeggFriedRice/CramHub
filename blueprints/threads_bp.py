from flask import Blueprint, jsonify, request
from init import db
from models.threads import Thread, ThreadSchema
from models.users import User, UserSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

threads = Blueprint('threads', __name__, url_prefix='/threads')

# Get all threads
@threads.route("/", methods=["GET"])
def get_all_threads():
    stmt = db.select(Thread)
    threads_list = db.session.scalars(stmt)
    result = ThreadSchema(many=True, exclude=["comments"]).dump(threads_list)
    return jsonify(result)

# Get a single thread
# @threads.route("/<int:id")
# pass


# Create new thread
@threads.route("/", methods=["POST"])
@jwt_required()
def create_thread():
    thread_fields = ThreadSchema(exclude=['id', 'date']).load(request.json)
    # Get user id from JWT
    user_id = get_jwt_identity()
    new_thread = Thread()
    new_thread.category = thread_fields["category"]
    new_thread.title = thread_fields["title"]
    new_thread.date = date.today()
    new_thread.description = thread_fields["description"]
    new_thread.link = thread_fields["link"]
    new_thread.user_id = user_id

    db.session.add(new_thread)
    db.session.commit()
    return jsonify(
        ThreadSchema().dump(new_thread),
        {"CramHub Message": "Thread submitted! 🙂"}), 201

# Update existing thread
@threads.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_thread(id):
    thread_info = ThreadSchema(exclude=['id', 'date']).load(request.json)
    stmt = db.select(Thread).filter_by(id=id)
    thread = db.session.scalar(stmt)
    if thread:
        thread.category = thread_info.get('category', thread.category)
        thread.title = thread_info.get('title', thread.title)
        thread.description = thread_info.get('description', thread.description)
        thread.link = thread_info.get('link', thread.link)
        db.session.commit()
        return jsonify(
            ThreadSchema().dump(thread),
            {"CramHub Message": f"Thread '{thread.title}' has been updated! 🙂"})
    else:
        return {"CramHub Message": "Thread not found! 😯"}, 404

# Delete existing thread
@threads.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_thread(id):
    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if not user or not user.admin:
        return {'CramHub Message': "You can't delete this thread! 😔"}

    stmt = db.select(Thread).filter_by(id=id)
    thread = db.session.scalar(stmt)
    if not thread:
        return {"CramHub Message": "Thread not found 😯"}

    db.session.delete(thread)
    db.session.commit()
    return jsonify(
        ThreadSchema().dump(thread),
        {"CramHub Message": f"Thread '{thread.title}' deleted 🙂"})