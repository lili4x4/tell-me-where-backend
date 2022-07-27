from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False),
    friend_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    friends = relationship("User")
    # recs = db.relationship("Rec", back_populates='user')
# Need to look more into many-to-many relationships

def self_to_dict(self):
        instance_dict = dict(
            id=self.id,
            username=self.username,
        )

        friend_list = [friend.self_to_dict() for friend in self.friends] if self.friends else []
        instance_dict["friends"] = friend_list
        
        return instance_dict