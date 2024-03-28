from blueprints.auth_bp import auth
from blueprints.cli_bp import db_commands
from blueprints.comments_bp import comments
from blueprints.threads_bp import threads
from blueprints.users_bp import users
from flask import Flask, jsonify
from init import bcrypt, db, jwt, ma
from marshmallow.exceptions import ValidationError
from os import environ
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
        return jsonify({'Error': 'We couldn\'t find that on the system!'}), 404
    
    @app.errorhandler(401)
    def unauthorised(e):
        return jsonify({'Error': 'You don\'t have permission to do that!'}), 401 

    return app
