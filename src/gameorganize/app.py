from flask import Flask, render_template, request, url_for, redirect
from model.game import sessionmaker, GameEntry, Completion, Base, sa

app = Flask(__name__)
app.config['SECRET_KEY'] = '7103fd2f0697987fef0626de455aeb8617f8318c2ecaad41'
app.config['MAX_CONTENT_PATH'] = pow(10,7)
engine = sa.create_engine("sqlite:///games.sqlite3", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session() 

@app.route("/game/<id>", methods=['GET', 'POST'])
def game_detail(id):
  game = session.get(GameEntry, id)

  if(not game):
    return "Error: Game ID {} not found".format(id)

  if request.method == 'POST':
    game.name = request.form.get("name")
    game.platform = request.form.get("platform")
    game.completion = request.form.get("completion")
    game.cheev = request.form.get("cheev")
    game.cheev_total = request.form.get("cheev_total")
    game.notes = request.form.get("notes")
    session.commit()
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
    session.add(new_game)
    session.commit()
    return redirect(url_for('all_games', id=id))

  return render_template(
    'game/add.html',
    Completion=Completion
  )

@app.route("/game/<id>/delete", methods=['GET', 'POST'])
def game_delete(id):
  game = session.get(GameEntry, id)
  if(not game):
    return "Error: Game ID {} not found".format(id)
  
  session.delete(game)
  session.commit()

  return "Game ID {} deleted".format(id)

@app.route("/")
def all_games():
  all_games=session.query(GameEntry)

  return render_template(
    'list.html',
    all_games=all_games,
  )
