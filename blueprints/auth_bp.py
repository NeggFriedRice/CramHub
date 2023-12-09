from flask import Blueprint, abort
from init import db
from models.users import User
from flask_jwt_extended import get_jwt_identity


# Authorisation blueprint registered in main
auth = Blueprint('auth', __name__)

def authorise(user_id=None):
    # Get user id from JWT
    jwt_user_id = get_jwt_identity()
    # Select user object from db that matches JWT user id
    stmt = db.select(User).filter_by(id=jwt_user_id)
    # Return selected user object
    user = db.session.scalar(stmt)
    # Abort if user is not admin or JWT user id does not match passed in user id
    if not (user.admin or (user_id and int(jwt_user_id) == user_id)):
        abort(401)