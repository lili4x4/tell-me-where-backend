from app import db
from datetime import datetime

user_to_user = db.Table("user_to_user", db.metadata,
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
)

user_rec = db.Table('user_rec',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('rec_id', db.Integer, db.ForeignKey('rec.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    friends = db.relationship("User",
                        secondary=user_to_user,
                        primaryjoin=id==user_to_user.c.follower_id,
                        secondaryjoin=id==user_to_user.c.friend_id,
                        backref="followers"
    )
    recs = db.relationship('Rec', secondary=user_rec, backref='user')

    required_attributes = {
        "username" : True,
    }

    def self_to_dict(self):
            instance_dict = dict(
                id=self.id,
                username=self.username,
            )

            friend_list = [friend.self_to_dict() for friend in self.friends] if self.friends else []
            instance_dict["friends"] = friend_list
            
            return instance_dict

    def follow(self, user):
            if not self.is_following(user):
                self.friends.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.friends.remove(user)

    def is_following(self, user):
        return self.friends.filter(
            followers.c.friend_id == user.id).count() > 0

    @classmethod
    def create_from_dict(cls, data_dict):
        if data_dict.keys() == cls.required_attributes.keys():
            return cls(username=data_dict["username"])
        else:
            remaining_keys= set(data_dict.keys())-set("username")
            response=list(remaining_keys)
            raise ValueError(response)    
    
    @classmethod
    def return_class_name(cls):
        return cls.__name__


class Rec(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_name = db.Column(db.String)
    yelp_id = db.Column(db.String)
    yelp_url = db.Column(db.String)
    price = db.Column(db.String)
    category1 = db.Column(db.String)
    category2 = db.Column(db.String)
    category3 = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.relationship('User', secondary=user_rec, backref='rec')