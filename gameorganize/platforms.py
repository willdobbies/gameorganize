from .db import db
from .model.user import User
from .model.platform import Platform, get_user_platforms
from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user

platforms = Blueprint('platforms', __name__, template_folder='templates')

@platforms.route("/<username>", methods=['GET', 'POST'])
def details(username):
  _user = db.session.query(User).where(User.username==username).first()
  return render_template(
    'user/platforms.html',
    username=_user.username,
    platforms=_user.platforms,
  )

@platforms.route("/add", methods=['POST'])
@login_required
def add():
  try:
    if(not request.form.get("name")):
      raise ValueError("Empty platform name")
    new_platform = Platform(
      name = request.form.get("name"),
      user_id = current_user.id,
    )
    db.session.add(new_platform)
    db.session.commit()
  except Exception as e:
    flash(f"DB Error: {e}")
    return redirect(url_for('platforms.details', username=current_user.username))

  flash(f"Added new platform {new_platform.name}")
  return redirect(url_for('platforms.details', username=current_user.username))

@platforms.route("/<id>/delete", methods=['POST'])
@login_required
def delete(id):
  platform = db.session.get(Platform, id)

  if(not platform):
    abort(404)

  if(platform.user_id != current_user.id):
    abort(403)
  
  db.session.delete(platform)
  db.session.commit()

  flash(f"Deleted platform {platform.name}")
  return redirect(url_for('platforms.details', username=current_user.username))