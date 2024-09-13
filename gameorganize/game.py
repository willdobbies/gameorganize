from flask import Blueprint, render_template, request, url_for, redirect, flash
from .model.game import GameEntry, Completion, Priority
from .db import db

game = Blueprint('game', __name__, template_folder='templates')

@game.route("/<id>", methods=['GET', 'POST'])
def detail(id):
  game = db.session.get(GameEntry, id)
  #game = db.one_or_404(db.select(GameEntry).filter_by(id=id))

  if(not game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('gamelist.detail'))

  if request.method == 'POST':
    game.name = request.form.get("name")
    game.platform = request.form.get("platform")
    game.completion = request.form.get("completion")
    game.priority = request.form.get("priority")
    game.cheev = request.form.get("cheev")
    game.cheev_total = request.form.get("cheev_total")
    game.notes = request.form.get("notes")
    db.session.commit()
    flash(f"Updated: Game {game.name}")
    return redirect(url_for('game.detail', id=id))

  return render_template(
    'game/detail.html',
    game=game,
    Completion=Completion,
    Priority=Priority
  )

@game.route("/add", methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
    new_game = GameEntry(
      name = request.form.get("name"),
      platform = request.form.get("platform"),
      completion = request.form.get("completion"),
      priority = request.form.get("priority"),
      cheev = request.form.get("cheev"),
      cheev_total = request.form.get("cheev_total"),
      notes = request.form.get("notes"),
    )
    try:
      db.session.add(new_game)
      db.session.commit()
    except Exception as e:
      flash(f"DB Error: {e}")
      return redirect(url_for('game.add'))

    flash(f"Added new game {new_game.name}")
    return redirect(url_for('gamelist.detail'))

  return render_template(
    'game/add.html',
    Completion=Completion,
    Priority=Priority
  )

@game.route("/<id>/delete", methods=['GET', 'POST'])
def delete(id):
  game = db.session.get(GameEntry, id)

  if(not game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('gamelist.detail'))
  
  db.session.delete(game)
  db.session.commit()

  flash(f"Deleted game {game.name}")
  return redirect(url_for('gamelist.detail'))