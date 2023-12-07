from flask import Blueprint, jsonify, request, abort
from init import db
from models.users import User, UserSchema
from models.threads import Thread, ThreadSchema

users = Blueprint('users', __name__, url_prefix='/users')

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
        result = ThreadSchema(many=True).dump(threads)
        return jsonify(result)
    else:
        return {"CramHub Message": "User not found! 😯"}, 404


# Get all comments made by users
@users.route("/comments", methods=["GET"])
def get_all_users_comments():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    result = UserSchema(many=True, exclude=["password", "admin", "id", "threads"]).dump(users_list)
    return jsonify(result)