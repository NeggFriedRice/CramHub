from flask import Blueprint, jsonify, request, abort
from init import db
from models.users import User, UserSchema
from main import bcrypt, jwt
from flask_jwt_extended import create_access_token
from datetime import timedelta
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
    
@auth.route('/login', methods=['POST'])
def login():
    user_fields = UserSchema().load(request.json)
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    if not user or not bcrypt.check_password_hash(user.password, user_fields['password']):
        return {"CramHUB Message": "Invalid username or password!"}, 401
    
    expiry = timedelta(hours=6)

    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"user": user.email, "token": access_token},
                   {"CramHub Message": "Successfully logged in!"})
    
