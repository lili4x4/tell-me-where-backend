from flask import Blueprint, request, jsonify, make_response
from app import db
from app.helper_functions import *
from app.models.user_and_rec_models import Rec

rec_bp = Blueprint('Recs', __name__, url_prefix='/recs')

@rec_bp.route("", methods=["GET"])
def get_recs():
    recs = Rec.query.all()
    recs_response = [rec.self_to_dict() for rec in recs]
    return success_message_info_as_list(recs_response, status_code=200)

@rec_bp.route("/<id>", methods=["DELETE"])
def delete_rec(id):
    rec = get_record_by_id(Rec, id)
    db.session.delete(rec)
    db.session.commit()
    
    return success_message_info_as_list(dict(details=f'Rec {rec.id} successfully deleted'))
