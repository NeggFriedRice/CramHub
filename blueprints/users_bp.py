from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from models.threads import Thread, ThreadSchema
from models.users import User, UserSchema
from sqlalchemy.exc import IntegrityError


users = Blueprint('users', __name__, url_prefix='/users')

# Register new user
@users.route('/register', methods=['POST'])
def register():
    try:
        # Parse and validate request body through UserSchema
        user_fields = UserSchema().load(request.json)
        # Create new user object
        user = User()
        # Assign incoming attributes from request body to new user object
        user.name = user_fields['name']
        user.password = bcrypt.generate_password_hash(user_fields['password']).decode("utf-8")
        user.email = user_fields['email']
        user.cohort = user_fields['cohort']
        user.admin = False
        # Add new user object to db
        db.session.add(user)
        # Commit updates
        db.session.commit()
        # Set 6 hour expiry variable
        expiry = timedelta(hours=6)
        # Create access token for user
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        # Return JSNOified new user object, successful registration message and access token
        return jsonify(
            UserSchema(exclude=['password', 'admin']).dump(user),
            {'Message': f"User {user.name} has been registered! 🙂"},
            {'Access token': access_token}), 201
    # Error handler if user already exists
    except IntegrityError:
        return {'Error': 'This user already exists😯'}, 409

# Log in user
@users.route('/login', methods=['POST'])
def login():
    # Load incoming JSON request body and validate through UserSchema
    user_fields = UserSchema(exclude=["name", "cohort"]).load(request.json)
    # Select user object from db that matches JSON body email
    stmt = db.select(User).filter_by(email=request.json['email'])
    # Return user object
    user = db.session.scalar(stmt)
    # Check if user exists and if the hashed password matches hashed JSON body password
    if not user or not bcrypt.check_password_hash(user.password, user_fields['password']):
        # If user does not exist or password is incorrect, show error message
        return {"Error": "Invalid username or password! 😯"}, 401
    # Set 6 hour expiry variable
    expiry = timedelta(hours=6)
    # Create access token for user
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # Return user email, access token and successful log in message to user
    return jsonify({"user": user.email, "token": access_token},
                   {"Message": "Successfully logged in! 🙂"})

# Get all users
@users.route("/", methods=["GET"])
def get_all_users():
    # Select all user objects from db
    stmt = db.select(User)
    # Return all selected user objects
    users_list = db.session.scalars(stmt)
    # Parse user objects through UserSchema (exclude threads and comments)
    result = UserSchema(many=True, exclude=["password", "admin", "threads", "comments"]).dump(users_list)
    # Display JSONified user objects
    return jsonify(result)

# Get all threads made by users
@users.route("/threads", methods=["GET"])
def get_all_users_threads():
    # Select all user objects from db
    stmt = db.select(User)
    # Return all selected user objects
    users_list = db.session.scalars(stmt)
    # Parse user objects through UserSchema (exclude comments)
    result = UserSchema(many=True, exclude=["password", "admin", "id", "comments"]).dump(users_list)
    return jsonify(result)

# Get threads made by single user
@users.route("/<int:id>/threads", methods=["GET"])
def get_user_threads(id):
    # Select user object from db that matches passed in id
    stmt = db.select(User).filter_by(id=id)
    # Return selected user object
    user = db.session.scalar(stmt)
    # Check if user exists
    if user:
        # Select thread objects from db that have a user_id that matches passed in id
        stmt = db.select(Thread).where(Thread.user_id == id)
        # Return selected thread objects
        threads = db.session.scalars(stmt)
        # Parse thread objects through ThreadSchema (exclude comments)
        result = ThreadSchema(many=True, exclude=['comments']).dump(threads)
        # Display JSONified thread objects
        return jsonify(result)
    # If user does not exist, show error message
    else:
        return {"Error": "User not found! 😯"}, 404

# Get all comments made by users
@users.route("/comments", methods=["GET"])
def get_all_users_comments():
    # Select all user objects from db
    stmt = db.select(User)
    # Return all selected user objects
    users_list = db.session.scalars(stmt)
    # Parse user objects through UserSchema (exclude threads)
    result = UserSchema(many=True, exclude=["password", "admin", "id", "threads"]).dump(users_list)
    # Display JSONified user objects
    return jsonify(result)