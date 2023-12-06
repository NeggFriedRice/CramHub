from init import db, ma


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    rating = db.Column(db.Integer)
    review = db.Column(db.String())

# Create comment schema with Marshmallow
class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "rating", "review")

