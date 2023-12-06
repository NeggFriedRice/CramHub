from flask import Blueprint, jsonify, request
from main import db
from models.users import User

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['GET'])
def get_users():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)