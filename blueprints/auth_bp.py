from flask import Blueprint, jsonify, request, abort
from init import db
from models.users import User, UserSchema
from main import bcrypt, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)

# Register new user
@auth.route('/register', methods=['POST'])
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
            {'CramHub Message': f"User {user.name} has been registered! 🙂"},
            {'Access token': access_token}), 201
    
    except IntegrityError:
        return {'Error encountered': 'This user already exists😯'}, 409

# Log in user
@auth.route('/login', methods=['POST'])
def login():
    user_fields = UserSchema(exclude=["name", "cohort"]).load(request.json)
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    if not user or not bcrypt.check_password_hash(user.password, user_fields['password']):
        return {"CramHUB Message": "Invalid username or password! 😯"}, 401
    
    expiry = timedelta(hours=6)

    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"user": user.email, "token": access_token},
                   {"CramHub Message": "Successfully logged in! 🙂"})
    
def authorise(user_id=None):
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    print(user)
    print(user_id)
    print(jwt_user_id)
    print(user.admin)
    if not (user.admin or (user_id and int(jwt_user_id) == user_id)):
        abort(jsonify(message="You don't have permission to do that! 😯"), 401)