from .db import db
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform, get_user_platforms
from .model.user import User
from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user

game = Blueprint('game', __name__, template_folder='templates')

@game.route("/<id>", methods=['GET'])
def detail(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    abort(404)

  _game_user = db.session.get(User, _game.user_id)

  return render_template(
    'game/detail.html',
    game=_game,
    game_user=_game_user,
    platforms=current_user.platforms,
    Completion=Completion,
    Priority=Priority,
  )

@game.route("/<id>", methods=['POST'])
@login_required
def update(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    abort(404)

  if(_game.user_id != current_user.id):
    abort(403)

  try:
    if(not request.form.get("name")):
      raise ValueError("Empty game name")
    _game.name = request.form.get("name")
    _game.platform_id = request.form.get("platform")
    _game.completion = request.form.get("completion")
    _game.priority = request.form.get("priority")
    _game.cheev = request.form.get("cheev")
    _game.cheev_total = request.form.get("cheev_total")
    _game.notes = request.form.get("notes")
    db.session.commit()
  except Exception as e:
    flash(f"DB Error: {e}")
    return redirect(url_for('game.detail', id=id))

  flash(f"Updated game: '{_game.name}'")
  return redirect(url_for('game.detail', id=id))


@game.route("/<id>/delete", methods=['POST'])
@login_required
def delete(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    abort(404)

  if(_game.user_id != current_user.id):
    abort(403)

  db.session.delete(_game)
  db.session.commit()

  flash(f"Deleted game '{_game.name}'")
  return redirect(url_for("user.detail", username=current_user.username))

@game.route("/add", methods=['GET'])
@login_required
def add():
  return render_template(
    'game/add.html',
    Completion=Completion,
    Priority=Priority,
    platforms=current_user.platforms,
  )

@game.route("/add", methods=['POST'])
@login_required
def add_post():
  try:
    if(not request.form.get("name")):
      raise ValueError("Empty game name")
    new_game = GameEntry(
      name = request.form.get("name"),
      platform_id = request.form.get("platform"),
      user_id = current_user.id,
      completion = request.form.get("completion"),
      priority = request.form.get("priority"),
      cheev = request.form.get("cheev"),
      cheev_total = request.form.get("cheev_total"),
      notes = request.form.get("notes"),
    )
    db.session.add(new_game)
    db.session.commit()
  except Exception as e:
    flash(f"DB Error: {e}")
    return redirect(url_for('game.add'))

  flash(f"Added new game {new_game.name}")
  return redirect(url_for('user.detail', username=current_user.username))