from app import db
from datetime import datetime
from app.helper_functions_api import *

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
                        backref=db.backref('followers', lazy='dynamic'),
                        lazy='dynamic'
    )
    recs = db.relationship('Rec', secondary=user_rec, backref='User')

    required_attributes = {
        "username" : True,
    }

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def self_to_dict(self):
            instance_dict = dict(
                id=self.id,
                username=self.username,
                recs=self.recs
            )

            friend_list = [friend.friend_to_dict() for friend in self.friends] if self.friends else []
            instance_dict["friends"] = friend_list
            
            recs_list = [rec.self_to_dict() for rec in self.recs] if self.recs else []
            instance_dict["recs"] = recs_list
            
            return instance_dict

    def friend_to_dict(self):
        friend_dict = dict(
            id=self.id,
            username=self.username,
        )
        return friend_dict

    def follow(self, user):
        if not self.is_following(user):
            self.friends.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.friends.remove(user)

    def is_following(self, user):
        return self.friends.filter(
            user_to_user.c.friend_id == user.id).count() > 0

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
    image_url = db.Column(db.String)
    users = db.relationship('User', secondary=user_rec, backref='Rec')

    def __repr__(self):
        return '<Rec {}>'.format(self.id)

    def self_to_dict(self):
        instance_dict = dict(
            id=self.id,
            restaurant_name=self.restaurant_name,
            # user=self.user.username,
            image_url=self.image_url,
            yelp_id=self.yelp_id,
            yelp_url=self.yelp_url,
            price=self.price,
            category1=self.category1,
            category2=self.category2,
            category3=self.category3,
            timestamp=self.timestamp,
        )

        user_list = [user.friend_to_dict() for user in self.users] if self.users else []
        instance_dict["users"] = user_list

        return instance_dict

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    def friend_to_dict(self):
        user_dict = dict(
            id=self.id,
            username=self.username,
        )
        return user_dict
        

    # @classmethod
    # def create_rec(data_dict):
    #     return Rec(
    #         username=data_dict["username"],
    #         restaurant_name=data_dict["restaurant_name"],
    #         image_url=data_dict["image_url"],
    #         yelp_id=data_dict["yelp_id"],
    #         yelp_url=data_dict["yelp_url"],
    #         price=data_dict["price"],
    #         category1=data_dict["category1"],
    #     )


