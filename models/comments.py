from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Length


# Valid ratings for comments
VALID_RATINGS = (1, 2, 3, 4, 5)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="comments")
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.id"), nullable=False)
    thread = db.relationship("Thread", back_populates="comments")

# Comment schema
class CommentSchema(ma.Schema):
    # Validate: rating field cannot be empty and must be one of VALID_RATINGS
    rating = fields.Integer(required=True, validate=OneOf(VALID_RATINGS))
    # Validate: review field cannot be empty and must be at least 1 character long
    review = fields.String(required=True, validate=Length(min=1, error='Please add a few words to your review! 🙂'))

    class Meta:
        ordered = True
        fields = ("id", "date", "thread", "user", "rating", "review")
    # Nested field for user and thread
    user = fields.Nested("UserSchema", only=["name"])
    thread = fields.Nested("ThreadSchema", only=["title"])
