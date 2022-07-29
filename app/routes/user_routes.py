from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.models import User
from app.helper_functions import *

user_bp = Blueprint('Users', __name__, url_prefix='/users')

# create a user
@user_bp.route("", methods=["POST"])
def create_new_user():
    try:
        request_body = request.get_json()
        new_user = User(
            username=request_body["username"],
            )
    except: 
        error_message({"details": "Invalid data"}, 400)

    db.session.add(new_user)
    db.session.commit()

    return success_message_info_as_list(dict(user=new_user.self_to_dict()), 201)

# read all users
@user_bp.route("", methods=["GET"])
def get_users():
    users = User.query.all()
    users_response = [user.self_to_dict() for user in users]
    return success_message_info_as_list(users_response, status_code=200)

# read one user
@user_bp.route("/<id>", methods=["GET"])
def get_user_by_id(id):
    user = get_record_by_id(User, id)

    return return_database_info_dict("user", user.self_to_dict())

# follow a user
@user_bp.route("/<id>/follow", methods=["PATCH"])
def follow_user_route(id):
    user = get_record_by_id(User, id)
    request_body = request.get_json()

    friend_id = request_body["id"]
    friend = get_record_by_id(User, friend_id)
    
    user.follow(friend)
    db.session.commit()

    return return_database_info_dict("user", user.self_to_dict())

# delete a user
@user_bp.route("/<id>", methods=["DELETE"])
def delete_user(id):
    user = get_record_by_id(User, id)
    db.session.delete(user)
    db.session.commit()
    
    return success_message_info_as_list(dict(details=f'User {user.id} successfully deleted'))
