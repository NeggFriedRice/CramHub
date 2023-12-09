from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And
from sqlalchemy.orm import validates


# Valid categories for threads
VALID_CATEGORIES = ("HTML", "CSS", "PYTHON", "SQL", "FLASK")

class Thread(db.Model):
    __tablename__ = "threads"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.String(), nullable=False)
    link = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="threads")
    comments = db.relationship("Comment", back_populates="thread", cascade="all, delete")
    
    # Custom validator: Convert category to uppercase
    @validates('category')
    def convert_upper(self, key, value):
        return value.upper()

# Thread schema
class ThreadSchema(ma.Schema):   
    # Validate: category cannot be empty string and must be one of VALID_CATEGORIES
    category = fields.String(required=True, validate=And(Length(min=1, error='Category can\'t be blank! 😯'), OneOf(VALID_CATEGORIES)))
    # Validate: title cannot be empty string
    title = fields.String(required=True, validate=Length(min=1, error='Title can\'t be blank! 😯'))
    # Validate: description cannot be empty string
    description = fields.String(required=True, validate=Length(min=1, error='Please add a few words to your thread! 🙂'))
       
    class Meta:
        ordered = True
        fields = ("id", "category", "title", "date", "user", "description", "link", "comments")
    # Nested fields for user and comments
    user = fields.Nested("UserSchema", only=["name"])
    comments = fields.List(fields.Nested("CommentSchema", exclude=["thread"]))


