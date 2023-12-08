from init import db, ma
from marshmallow import fields


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    rating = db.Column(db.Integer)
    review = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="comments")
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.id"), nullable=False)
    thread = db.relationship("Thread", back_populates="comments", cascade="all, delete")

# Create comment schema with Marshmallow
class CommentSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "date", "rating", "user", "review", "thread")
    user = fields.Nested("UserSchema", only=["name"])
    thread = fields.Nested("ThreadSchema", only=["title"])
