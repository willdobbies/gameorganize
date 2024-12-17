from .db import db
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform, get_user_platforms
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user

game = Blueprint('game', __name__, template_folder='templates')

@game.route("/<username>/game/<id>", methods=['GET', 'POST'])
@login_required
def detail(username, id):
  _game = db.session.get(GameEntry, id)
  #game = db.one_or_404(db.select(GameEntry).filter_by(id=id))
  print(_game)

  if(not _game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('user.detail'))

  if request.method == 'POST':
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
      return redirect(url_for('game.detail', username=username, id=id))

    flash(f"Updated: Game {_game.name}")
    return redirect(url_for('game.detail', username=username, id=id))

  return render_template(
    'game/detail.html',
    game=_game,
    username=username,
    platforms=current_user.platforms,
    Completion=Completion,
    Priority=Priority,
  )

@game.route("/<username>/game/add", methods=['GET', 'POST'])
@login_required
def add(username):
  if request.method == 'POST':
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
      return redirect(url_for('game.add', username=username))

    flash(f"Added new game {new_game.name}")
    return redirect(url_for('user.detail', username=username))

  return render_template(
    'game/add.html',
    Completion=Completion,
    Priority=Priority,
    username=username,
    platforms=current_user.platforms,
  )

@game.route("/<username>/game/<id>/delete", methods=['GET', 'POST'])
@login_required
def delete(username, id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('user.detail'))
  
  db.session.delete(_game)
  db.session.commit()

  flash(f"Deleted game {_game.name}")
  return redirect(url_for('user.detail', username=username))