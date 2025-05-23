from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from gameorganize.db import db
from gameorganize.model.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint('auth', __name__)

rex_password = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")

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
    return redirect(url_for('user.detail', username=current_user.username))

#@auth.route('/login')
#def login():
#    return render_template('auth/login.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")

    # check if username unique
    user = User.query.filter_by(username=username).first()
    
    if(not username):
        flash(f"Username must not be empty")
        return redirect(url_for('home'))
    
    if(not rex_password.match(password)):
        flash(f"Password must be at least 8 characters long and contain numbers and uppercase letters")
        return redirect(url_for('home'))

    if(user):
        flash(f"User {user.username} already exists")
        return redirect(url_for('home'))
    
    # make new user!
    new_user = User(
        username=username,
        password=generate_password_hash(password, method='pbkdf2:sha1')
    )

    db.session.add(new_user)
    db.session.commit()
    
    # send to login page
    flash(f"User {new_user.username} created. You can now log in.")
    return redirect(url_for('home'))

#@auth.route('/signup')
#def signup():
#    return render_template('auth/signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))