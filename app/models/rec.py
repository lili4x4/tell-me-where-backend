from app import db

class Rec(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_name = db.Column(db.String)
    yelp_id = db.Column(db.String)
    yelp_url = db.Column(db.String)
    price = db.Column(db.String)
    category1 = db.Column(db.String)
    category2 = db.Column(db.String)
    category3 = db.Column(db.String)


    # username = db.Column(db.String, nullable=False),