from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User
from app.helper_functions import success_message_info_as_list, error_message

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

