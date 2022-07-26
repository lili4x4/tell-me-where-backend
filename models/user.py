from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False),
    # friends = db.relationship("Friend", back_populates='user'

# Need to look more into many-to-many relationships