from flask import Blueprint, render_template, url_for, request, redirect, flash
import os
from flask import current_app as app
from ..model import User
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

auth_bp = Blueprint('auth_bp', __name__,template_folder='templates',static_folder='static')

@auth_bp.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@auth_bp.route('/login')
def login():
    return  render_template("login.html")

@auth_bp.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'errors')
        return redirect(url_for('auth_bp.login'))
    login_user(user)
    flash('Login Successfully', 'success')
    return redirect(url_for('home_bp.profile'))


@auth_bp.route('/signup')
def signup():
    return render_template('signup.html')

@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exist", 'errors')
        return redirect(url_for('auth_bp.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/logout')
def logout():
    return 'Logout'
