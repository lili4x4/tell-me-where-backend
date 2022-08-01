from flask import Blueprint, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash, flash, login_required, logout_user
from app.models.models import User
from . import db
from flask_login import login_user



auth = Blueprint('auth', __name__)

#login  page
@auth.route('/login')
def login():
    return 'Login'

#login post request
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))


#logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


#sign up page
@auth.route('/signup')
def signup():
    return 'Signup'

#sign up post request
@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the username already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))
