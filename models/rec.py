from app import db

class Rec(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username = db.Column(db.String, nullable=False),