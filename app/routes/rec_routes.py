from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.models import Rec
from app.helper_functions import *
# from flask_login import current_user
from flask.ext.login import current_user


rec_bp = Blueprint('Recs', __name__, url_prefix='/recs')

#get all user recs
@rec_bp.route("", methods=["GET"])
def get_user_recs():
    user_recs = Rec.query.filter_by(user=current_user.id)
    return jsonify(user_recs)

    



