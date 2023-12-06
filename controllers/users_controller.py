from flask import Blueprint, jsonify, request, abort
from main import db
from models.users import User
from schemas.user_schema import UserSchema

users = Blueprint('users', __name__, url_prefix='/users')

@users.route("/", methods=["GET"])
def get_users():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    result = UserSchema(many=True).dump(users_list)

    return jsonify(result)
