from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from gameorganize.db import db
from gameorganize.model.user import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    # fetch user login form data
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check username/password
    if not username:
        flash(f"Empty username")
        return redirect(url_for('home')) 

    # find matching user
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(f"User '{username}' does not exist!")
        return redirect(url_for('home')) 
    
    if not check_password_hash(user.password_hash, password):
        flash('Invalid username or password')
        return redirect(url_for('home')) 

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

    user = User.query.filter_by(username=username).first()
    
    if(user):
        flash(f"User {user.username} already exists")
        return redirect(url_for('home'))
    
    # make new user!
    try:
        new_user = User(
            username=username,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        flash(str(e))
        return redirect(url_for('home'))
    
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