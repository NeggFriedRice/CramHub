from flask import Blueprint, jsonify, request, abort
from init import db
from models.users import User, UserSchema
from main import bcrypt, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta


auth = Blueprint('auth', __name__)

def authorise(user_id=None):
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    print(user)
    print(user_id)
    print(jwt_user_id)
    print(user.admin)
    if not (user.admin or (user_id and int(jwt_user_id) == user_id)):
        abort(401)