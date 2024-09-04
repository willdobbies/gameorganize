from flask import Flask, render_template, request, url_for, redirect, flash
from model.db import db
from model.game import GameEntry, Completion

app = Flask(__name__)
app.config['SECRET_KEY'] = '7103fd2f0697987fef0626de455aeb8617f8318c2ecaad41'
app.config['MAX_CONTENT_PATH'] = pow(10,7)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.sqlite3"

# setup sqlalchemy
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/game/<id>", methods=['GET', 'POST'])
def game_detail(id):
  game = db.session.get(GameEntry, id)

  if(not game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('all_games'))

  if request.method == 'POST':
    game.name = request.form.get("name")
    game.platform = request.form.get("platform")
    game.completion = request.form.get("completion")
    game.cheev = request.form.get("cheev")
    game.cheev_total = request.form.get("cheev_total")
    game.notes = request.form.get("notes")
    db.session.commit()
    flash(f"Updated: Game {game.name}")
    return redirect(url_for('game_detail', id=id))

  return render_template(
    'game/detail.html',
    game=game,
    Completion=Completion
  )

@app.route("/game/add", methods=['GET', 'POST'])
def game_add():
  if request.method == 'POST':
    new_game = GameEntry(
      name = request.form.get("name"),
      platform = request.form.get("platform"),
      completion = request.form.get("completion"),
      cheev = request.form.get("cheev"),
      cheev_total = request.form.get("cheev_total"),
      notes = request.form.get("notes"),
    )
    db.session.add(new_game)
    db.session.commit()
    flash(f"Added new game {new_game.name}")
    return redirect(url_for('all_games', id=id))

  return render_template(
    'game/add.html',
    Completion=Completion
  )

@app.route("/game/<id>/delete", methods=['GET', 'POST'])
def game_delete(id):
  game = db.session.get(GameEntry, id)

  if(not game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('all_games'))
  
  db.session.delete(game)
  db.session.commit()

  flash(f"Deleted game {game.name}")
  return redirect(url_for('all_games'))

@app.route("/")
def all_games():
  all_games=db.session.query(GameEntry)

  return render_template(
    'list.html',
    all_games=all_games,
  )
