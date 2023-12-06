from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database object
db = SQLAlchemy()

def create_app():
    # Create flask app object
    app = Flask(__name__)

    # Configure app
    app.config.from_object("config.app_config")

    # Creating our database object
    db.init_app(app)

    return app
