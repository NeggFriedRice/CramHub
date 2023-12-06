from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users
from blueprints.threads_bp import threads
from blueprints.comments_bp import comments

def setup():
    # Create flask app object
    app = Flask(__name__)

    # Configure app
    app.config['JWT_SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

    # Creating our database object
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
   
    app.register_blueprint(db_commands)
    app.register_blueprint(users)
    app.register_blueprint(threads)
    app.register_blueprint(comments)

    return app
