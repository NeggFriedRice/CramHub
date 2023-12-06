from init import db, ma
from marshmallow.validate import Length

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    cohort = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean(), default=False)

# Create user schema with Marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "password", "email", "cohort")
        password = ma.String(validate=Length(min=6))
