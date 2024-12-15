from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required
from gameorganize.db import db
from gameorganize.model.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    # fetch user login form data
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # find matching user
    user = User.query.filter_by(username=username).first()

    # check password
    if not user or not check_password_hash(user.password, password):
        flash('Invalid username or password')
        return redirect(url_for('auth.login')) 

    # send to homepage
    login_user(user, remember=remember)
    return redirect(url_for('gamelist.detail'))

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")

    # check if username unique
    user = User.query.filter_by(username=username).first()

    if(user):
        flash(f"User {user.username} already exists")
        return redirect(url_for('auth.signup'))
    
    # make new user!
    new_user = User(
        username=username,
        password=generate_password_hash(password, method='pbkdf2:sha1')
    )

    db.session.add(new_user)
    db.session.commit()
    
    # send to login page
    flash(f"User {new_user.username} created. You can now log in.")
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))