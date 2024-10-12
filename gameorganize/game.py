from flask import Blueprint, render_template, request, url_for, redirect, flash
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform
from .db import db

game = Blueprint('game', __name__, template_folder='templates')

@game.route("/<id>", methods=['GET', 'POST'])
def detail(id):
  _game = db.session.get(GameEntry, id)
  #game = db.one_or_404(db.select(GameEntry).filter_by(id=id))
  print(_game)

  if(not _game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('gamelist.detail'))

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
      return redirect(url_for('game.detail', id=id))

    flash(f"Updated: Game {_game.name}")
    return redirect(url_for('game.detail', id=id))

  all_platforms=db.session.query(Platform)

  return render_template(
    'game/detail.html',
    game=_game,
    all_platforms=all_platforms,
    Completion=Completion,
    Priority=Priority
  )

@game.route("/add", methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
    try:
      if(not request.form.get("name")):
        raise ValueError("Empty game name")
      new_game = GameEntry(
        name = request.form.get("name"),
        platform_id = request.form.get("platform"),
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
    return redirect(url_for('gamelist.detail'))

  all_platforms=db.session.query(Platform)

  return render_template(
    'game/add.html',
    all_platforms=all_platforms,
    Completion=Completion,
    Priority=Priority
  )

@game.route("/<id>/delete", methods=['GET', 'POST'])
def delete(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('gamelist.detail'))
  
  db.session.delete(_game)
  db.session.commit()

  flash(f"Deleted game {_game.name}")
  return redirect(url_for('gamelist.detail'))