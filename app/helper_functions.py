from flask import jsonify, abort, make_response
import os
import requests


def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message_info_as_list(message, status_code=200):
    return make_response(jsonify(message), status_code)

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    record = cls.query.get(id)
    if record:
        return record
    else:
        error_message(f"{cls.return_class_name()} id: {id} not found", 404)

def return_database_info_dict(category, return_value):
    return_dict = {}
    return_dict[category] = return_value
    return make_response(jsonify(return_dict))