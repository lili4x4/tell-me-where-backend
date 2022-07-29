from flask import jsonify, abort, make_response
import os
import requests


def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message_info_as_list(message, status_code=200):
    return make_response(jsonify(message), status_code)