from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    cohort = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean(), default=False)

