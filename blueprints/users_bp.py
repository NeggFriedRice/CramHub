from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity
from init import db
from models.users import User, UserSchema
from models.threads import Thread, ThreadSchema
from datetime import timedelta
from main import bcrypt, jwt
from sqlalchemy.exc import IntegrityError

users = Blueprint('users', __name__, url_prefix='/users')

# Register new user
@users.route('/register', methods=['POST'])
def register():
    try:
        user_fields = UserSchema().load(request.json)
        user = User()
        user.name = user_fields['name']
        user.password = bcrypt.generate_password_hash(user_fields['password']).decode("utf-8")
        user.email = user_fields['email']
        user.cohort = user_fields['cohort']
        user.admin = False

        db.session.add(user)
        db.session.commit()

        expiry = timedelta(hours=6)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

        return jsonify(
            UserSchema(exclude=['password', 'admin']).dump(user),
            {'Error': f"User {user.name} has been registered! 🙂"},
            {'Access token': access_token}), 201
    
    # Error handling when user exist
    except IntegrityError:
        return {'Error encountered': 'This user already exists😯'}, 409

# Log in user
@users.route('/login', methods=['POST'])
def login():
    user_fields = UserSchema(exclude=["name", "cohort"]).load(request.json)
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    if not user or not bcrypt.check_password_hash(user.password, user_fields['password']):
        return {"Error": "Invalid username or password! 😯"}, 401
    
    expiry = timedelta(hours=6)

    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"user": user.email, "token": access_token},
                   {"Error": "Successfully logged in! 🙂"})

@users.route("/", methods=["GET"])
def get_all_users():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    result = UserSchema(many=True, exclude=["password", "admin", "threads", "comments"]).dump(users_list)
    return jsonify(result)

# Get all threads made by users
@users.route("/threads", methods=["GET"])
def get_all_users_threads():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    result = UserSchema(many=True, exclude=["password", "admin", "id", "comments"]).dump(users_list)
    return jsonify(result)

# Get threads made by single user
@users.route("/<int:id>/threads", methods=["GET"])
def get_user_threads(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        stmt = db.select(Thread).where(Thread.user_id == id)
        threads = db.session.scalars(stmt)
        result = ThreadSchema(many=True, exclude=['comments']).dump(threads)
        return jsonify(result)
    else:
        return {"Error": "User not found! 😯"}, 404

# Get all comments made by users
@users.route("/comments", methods=["GET"])
def get_all_users_comments():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    result = UserSchema(many=True, exclude=["password", "admin", "id", "threads"]).dump(users_list)
    return jsonify(result)