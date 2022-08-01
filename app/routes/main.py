from flask import Blueprint
from . import db
from flask_login import login_required, current_user



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Tell Me where'

@login_required
@main.route('/profile')
def profile():
    return ' User Profile'
