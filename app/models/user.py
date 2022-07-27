from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

user_to_user = db.Table("user_to_user", db.metadata,
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
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


def self_to_dict(self):
        instance_dict = dict(
            id=self.id,
            username=self.username,
        )

        friend_list = [friend.self_to_dict() for friend in self.friends] if self.friends else []
        instance_dict["friends"] = friend_list
        
        return instance_dict