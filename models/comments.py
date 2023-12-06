from main import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    rating = db.Column(db.Integer)
    review = db.Column(db.String())
