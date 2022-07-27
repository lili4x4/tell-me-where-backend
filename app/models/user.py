from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False),
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friends = relationship("User", remote_side=[id])


def self_to_dict(self):
        instance_dict = dict(
            id=self.id,
            username=self.username,
        )

        friend_list = [friend.self_to_dict() for friend in self.friends] if self.friends else []
        instance_dict["friends"] = friend_list
        
        return instance_dict