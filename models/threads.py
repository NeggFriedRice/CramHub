from init import db, ma


class Thread(db.Model):
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.String(), nullable=False)
    link = db.Column(db.String())

# Create thread schema with Marshmallow
class ThreadSchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "title", "date", "description", "link")