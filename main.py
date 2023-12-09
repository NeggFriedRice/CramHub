from flask import Flask, jsonify
from os import environ
from init import db, ma, bcrypt, jwt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users
from blueprints.threads_bp import threads
from blueprints.comments_bp import comments
from blueprints.auth_bp import auth
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

def setup():
    # Create flask app object
    app = Flask(__name__)

    # Configure app
    app.config['JWT_SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    app.json.sort_keys = False

    # Create our package objects
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(users)
    app.register_blueprint(auth)
    app.register_blueprint(threads)
    app.register_blueprint(comments)

    # Error handling
    @app.errorhandler(KeyError)
    def key_error(e):
        return {'Error': f'The field {e} is required'}, 400
    
    @app.errorhandler(ValidationError)
    def validation_error(e):
        return jsonify(e.messages), 400
    
    @app.errorhandler(BadRequest)
    def bad_request(e):
        return jsonify({'Error': str(e)}), 400
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'Error': 'We couldn\'t find that on the system!'})

   

    return app
