from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .model.platform import Platform
from .db import db

platform = Blueprint('platform', __name__, template_folder='templates')

@platform.route("/", methods=['GET', 'POST'])
@login_required
def detail():
  all_platforms=db.session.query(Platform).filter_by(user_id=current_user.id)

  return render_template(
    'platform/detail.html',
    all_platforms=all_platforms,
  )

@platform.route("/add", methods=['GET', 'POST'])
@login_required
def add():
  if request.method == 'POST':
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
      return redirect(url_for('platform.add'))

    flash(f"Added new game {new_platform.name}")
    return redirect(url_for('platform.detail'))

  return render_template(
    'platform/add.html',
  )

@platform.route("/<id>/delete")
@login_required
def delete(id):
  platform = db.session.query(Platform).where(Platform.id==id, Platform.user_id==current_user.id).first()

  if(not platform):
    flash(f"Error: Platform ID {id} not found")
    return redirect(url_for('platform.detail'))
  
  db.session.delete(platform)
  db.session.commit()

  flash(f"Deleted platform {platform.name}")
  return redirect(url_for('platform.detail'))