from flask import Blueprint, jsonify, request, abort
from init import db
from models.users import User, UserSchema
from main import bcrypt
from datetime import date
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        user_fields = UserSchema().load(request.json)
        user = User()
        user.name = user_fields['name']
        user.password = bcrypt.generate_password_hash(user_fields['password']).decode("utf-8")
        user.email = user_fields['email']
        user.cohort = user_fields['cohort']

        db.session.add(user)
        db.session.commit()

        return jsonify(
            UserSchema(exclude=['password', 'admin']).dump(user),
            {'CramHub Message': f"User {user.name} has been registered!"}), 201
    
    except IntegrityError:
        return {'Error encountered': 'This user already exists'}, 409