from main import db

class Thread(db.Model):
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(), nullable=False)
    link = db.Column(db.String())
