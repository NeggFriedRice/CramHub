from flask import Blueprint, jsonify, request
from init import db
from models.threads import Thread, ThreadSchema
from models.comments import Comment, CommentSchema
from models.users import User, UserSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import authorise


# Comments blueprint registered in main
threads = Blueprint('threads', __name__, url_prefix='/threads')

# Get all threads
@threads.route("/", methods=["GET"])
def get_all_threads():
    # Selects all threads objects from db
    stmt = db.select(Thread)
    # Returns all selected threads objects
    threads_list = db.session.scalars(stmt)
    # Parsed threads objects through Threadschema
    result = ThreadSchema(many=True, exclude=["comments"]).dump(threads_list)
    # Display JSONified result
    return jsonify(result)

# Get a single thread
@threads.route("/<int:id>")
def get_a_thread(id):
    # Selects thread from db that matches the passed in id
    stmt = db.select(Thread).where(Thread.id == id)
    # Return the selected thread
    thread = db.session.scalar(stmt)
    # If thread does not exist, return error message
    if not thread:
        return {"Error": "Thread not found! 😯"}, 404
    # Parse selected thread through ThreadSchema
    result = ThreadSchema().dump(thread)
    # Display JSONified result
    return jsonify(result)

# Create new thread
@threads.route("/", methods=["POST"])
@jwt_required()
def create_thread():
    # Convert incoming request 'category' to uppercase (used for OneOf validation)
    request.json["category"] = request.json["category"].upper()
    # Parse and validate request body through ThreadSchema
    thread_fields = ThreadSchema(exclude=['id', 'date']).load(request.json)
    # Get user id from JWT
    user_id = get_jwt_identity()
    # Create new thread object
    new_thread = Thread()
    # Assign incoming attributes from request body to new thread object
    new_thread.category = request.json["category"]
    new_thread.title = thread_fields["title"]
    new_thread.date = date.today()
    new_thread.description = thread_fields["description"]
    new_thread.link = thread_fields["link"]
    new_thread.user_id = user_id
    # Add new thread object to db
    db.session.add(new_thread)
    # Commit new thread object
    db.session.commit()
    # Display new JSONIfied thread and successful submission comment to user
    return jsonify(
        ThreadSchema(exclude=["user", "comments"]).dump(new_thread),
        {"Message": "Thread submitted! 🙂"}), 201

# Update existing thread
@threads.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_thread(id):
    # Convert incoming request 'category' to uppercase (used for OneOf validation)
    request.json["category"] = request.json["category"].upper()
    # Load incoming JSON request and validate through ThreadSchema
    thread_info = ThreadSchema(exclude=['id', 'date']).load(request.json)
    # Select thread from db that matches the passed in id
    stmt = db.select(Thread).filter_by(id=id)
    # Return selected thread
    thread = db.session.scalar(stmt)
    if thread:
        # If thread exists, authorise user
        authorise(thread.user_id)
        # Update thread attributes with incoming JSON body attributes
        thread.category = thread_info.get('category', thread.category)
        thread.title = thread_info.get('title', thread.title)
        thread.description = thread_info.get('description', thread.description)
        thread.link = thread_info.get('link', thread.link)
        # Commit updates
        db.session.commit()
    else:
        # If thread not found, show error message
        return {"Error": "Thread not found! 😯"}, 404
    # Display updated JSONified thread and successful update comment to user
    return jsonify(  
        ThreadSchema(exclude=["user", "comments", "date"]).dump(thread),
        {"Message": f"Thread '{thread.title}' has been updated! 🙂"})

# Delete existing thread
@threads.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_thread(id):
    # Select thread from db that matches the passed in id
    stmt = db.select(Thread).filter_by(id=id)
    # Return selected thread
    thread = db.session.scalar(stmt)
    if thread:
        # If thread exists, authorise user
        authorise(thread.user_id)
        # Delete selected thread
        db.session.delete(thread)
        # Commit updates
        db.session.commit()
    else:
        # If thread not found, show error message
        return {"Error": "Thread not found! 😯"}, 404
    # Display deleted thread title and successful delete comment to user
    return jsonify(
        {"Message": f"Thread '{thread.title}' deleted 🙂"})

# Create new comment on thread
@threads.route("/<int:thread_id>/comments", methods=["POST"])
@jwt_required()
def create_comment_on_thread(thread_id):
    # Load incoming JSON request and validate through ThreadSchema
    comment_fields = CommentSchema(exclude=['id', 'date']).load(request.json)
    # Get user id from JWT
    user_id = get_jwt_identity()
    # Create new comment object
    new_comment = Comment()
    # Update comment attributes with incoming JSON body attributes
    new_comment.rating = comment_fields["rating"]
    new_comment.review = comment_fields["review"]
    new_comment.user_id = user_id
    new_comment.thread_id = thread_id
    new_comment.date = date.today()
    # Add new comment object to db
    db.session.add(new_comment)
    # Commit updates
    db.session.commit()
    # Display new JSONified comment and successful submission comment to user
    return jsonify(
        CommentSchema().dump(new_comment),
        {"Message": "Comment submitted! 🙂"}), 201

# Get threads by category
@threads.route('/<category>')
def get_threads_by_category(category):
    # Convert passed in category to uppercase
    category = category.upper()
    # Select all threads objects with category that matches passed in category
    stmt = db.select(Thread).filter_by(category=category)
    # Return all selected threads objects
    threads = db.session.scalars(stmt)    
    # Parse threads objects through ThreadSchema
    result = ThreadSchema(many=True).dump(threads)
    # Display JSONified result
    return jsonify (result)

