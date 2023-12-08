from init import db, ma
from marshmallow import fields
from sqlalchemy.orm import validates


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
    comments = db.relationship("Comment", back_populates="thread")
    
    @validates('category')
    def convert_upper(self, key, value):
        return value.upper()

# Create thread schema with Marshmallow
class ThreadSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "category", "title", "date", "user", "description", "link", "comments")
    user = fields.Nested("UserSchema", only=["name"])
    comments = fields.List(fields.Nested("CommentSchema", exclude=["thread"]))