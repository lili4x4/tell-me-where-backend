from flask import Blueprint, request, jsonify, make_response, session
from sqlalchemy import JSON, column
from app import db
from app.helper_functions import *
from app.helper_functions_api import create_rec, create_rec_api_calls
from app.models.user_and_rec_models import User, Rec

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

# read one user by id
@user_bp.route("/<id>", methods=["GET"])
def get_user_by_id(id):
    user = get_record_by_id(User, id)

    return return_database_info_dict("user", user.self_to_dict())

# read one user by username
@user_bp.route("/usernames", methods=["GET"])
def get_user_by_username():
    user_query = request.args.get("username")
    if not user_query:
        return {"message": "must provide username parameter"}
    
    username = user_query
    user = get_record_by_username(username)

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

# unfollow a user
@user_bp.route("/<id>/unfollow", methods=["PATCH"])
def unfollow_user_route(id):
    user = get_record_by_id(User, id)
    request_body = request.get_json()

    friend_id = request_body["id"]
    friend = get_record_by_id(User, friend_id)
    
    user.unfollow(friend)
    db.session.commit()

    return return_database_info_dict("user", user.self_to_dict())


# delete a user
@user_bp.route("/<id>", methods=["DELETE"])
def delete_user(id):
    user = get_record_by_id(User, id)
    db.session.delete(user)
    db.session.commit()
    
    return success_message_info_as_list(dict(details=f'User {user.id} successfully deleted'))


##################################
#------------Rec Routes----------#
##################################

@user_bp.route("<id>/recs", methods=["POST"])
def create_rec_endpoint(id):
    user =  get_record_by_id(User, id)
    request_body = request.get_json()
    location = request_body["location"]
    search = request_body["search"]

    new_rec = create_rec_api_calls(location, search, user)
    
    return success_message_info_as_list(dict(rec=new_rec.self_to_dict()), 201)

@user_bp.route("<id>/recs", methods=["GET"])
def get_user_recs(id):
    user =  get_record_by_id(User, id)
    request_body = request.get_json()
    location = request_body["location"]
    search = request_body["search"]

    new_rec = create_rec_api_calls(location, search, user)
    
    return success_message_info_as_list(dict(rec=new_rec.self_to_dict()), 201)

