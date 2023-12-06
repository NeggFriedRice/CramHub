from flask import Blueprint, jsonify, request, abort
from init import db
from models.threads import Thread, ThreadSchema
from datetime import date

threads = Blueprint('threads', __name__, url_prefix='/threads')

@threads.route("/", methods=["GET"])
def get_threads():
    stmt = db.select(Thread)
    threads_list = db.session.scalars(stmt)
    result = ThreadSchema(many=True).dump(threads_list)

    return jsonify(result)

# Create new thread
@threads.route("/", methods=["POST"])
def create_thread():
    thread_fields = ThreadSchema(exclude=['id', 'date']).load(request.json)
    new_thread = Thread()
    new_thread.category = thread_fields["category"]
    new_thread.title = thread_fields["title"]
    new_thread.date = date.today()
    new_thread.description = thread_fields["description"]
    new_thread.link = thread_fields["link"]

    db.session.add(new_thread)
    db.session.commit()
    return jsonify(
        ThreadSchema().dump(new_thread),
        "Thread submitted!"), 201

# Update existing thread
@threads.route('/<int:id>', methods=['PUT', 'PATCH'])
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
            f"Thread '{thread.title}' has been updated"
        )
    else:
        abort(400, "Thread not found")

# Delete existing thread
@threads.route('/<int:id>', methods=['DELETE'])
def delete_thread(id):
    stmt = db.select(Thread).filter_by(id=id)
    thread = db.session.scalar(stmt)

    if not thread:
        abort(400, description="Thread not found")

    db.session.delete(thread)
    db.session.commit()
    return jsonify(
        ThreadSchema().dump(thread),
        f"Thread '{thread.title}' deleted"
    )