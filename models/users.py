from init import db, ma
from marshmallow.validate import Length
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    cohort = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    threads = db.relationship("Thread", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

# Create user schema with Marshmallow
class UserSchema(ma.Schema):
    name = fields.String(required=True, validate=Length(min=1, error='Name can\'t be blank! 😯'))
    password = fields.String(required=True, validate=Length(min=6, error='Password can\'t be blank and must have at least 6 characters! 😯'))
    email = fields.String(required=True, validate=Length(min=1, error='Email can\'t be blank! 😯'))
    cohort = fields.String(required=True, validate=Length(min=1, error='Cohort can\'t be blank! 😯'))


    class Meta:
        ordered = True
        fields = ("id", "name", "password", "email", "cohort", "admin", "threads", "comments")
        password = ma.String(validate=Length(min=6))
    threads = fields.List(fields.Nested("ThreadSchema", exclude=["user"]))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["user"]))
