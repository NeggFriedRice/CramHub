from flask import Blueprint, jsonify, request, abort
from init import db
from models.users import User, UserSchema

users = Blueprint('users', __name__, url_prefix='/users')

@users.route("/", methods=["GET"])
def get_users():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    result = UserSchema(many=True, exclude=["password", "admin"]).dump(users_list)

    return jsonify(result)
