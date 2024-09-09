from flask import Flask, render_template, request, url_for, redirect, flash
from importers.retroachievements import ImporterRetroAchievements as ImporterRA
from importers.steam import ImporterSteam
from model.game import GameEntry, Completion, Priority
from model.game import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '7103fd2f0697987fef0626de455aeb8617f8318c2ecaad41'
app.config['MAX_CONTENT_PATH'] = pow(10,7)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.sqlite3"

# setup sqlalchemy
db.init_app(app)

# Create the database tables.
with app.app_context():
  db.create_all()

@app.route("/game/<id>", methods=['GET', 'POST'])
def game_detail(id):
  game = db.session.get(GameEntry, id)
  #game = db.one_or_404(db.select(GameEntry).filter_by(id=id))

  if(not game):
    flash(f"Error: Game ID {id} not found")
    return redirect(url_for('all_games'))

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
    return redirect(url_for('game_detail', id=id))

  return render_template(
    'game/detail.html',
    game=game,
    Completion=Completion,
    Priority=Priority
  )

@app.route("/game/add", methods=['GET', 'POST'])
def game_add():
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
      return redirect(url_for('game_add'))

    flash(f"Added new game {new_game.name}")
    return redirect(url_for('all_games'))

  return render_template(
    'game/add.html',
    Completion=Completion,
    Priority=Priority
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

def add_or_update_game(new_game):
  # check if game name already exists
  dupe_game = db.session.query(GameEntry).filter_by(name="Hi").first()

  # update old entry if exists
  if(dupe_game):
    new_game.id = dupe_game.id
    dupe_game = new_game
  else:
    db.session.add(new_game)

  db.session.commit()

@app.route("/import", methods=['GET', 'POST'])
def game_import():
  if request.method == 'POST':
    site = request.form.get("website")
    apiId = request.form.get("id")
    apiKey = request.form.get("key")

    new_games = []

    try:
      if(site == "Steam"):
        importer = ImporterSteam(apiId, apiKey)
        fdata = importer.fetch()
        new_games = importer.parse(fdata)

      elif(site == "RetroAchievements"):
        importer = ImporterRA(username=apiId, api_key=apiKey)
        fdata = importer.fetch()
        new_games = importer.parse(fdata)

      else:
        flash(f"Invalid site {site}")
        return redirect(url_for('all_games'))

    except Exception as e:
      flash(f"Error importing from {site}, : {e}")
      return redirect(url_for('all_games'))

    for game in new_games:
      try:
        add_or_update_game(game)
      except Exception as e:
        flash(f"DB Errorr: {e}")

    flash(f"Imported {len(new_games)} games from {site}")
    return redirect(url_for('all_games'))

  return render_template(
    'import.html'
  )

def get_stats(games):
  perc = {}

  total = len([game for game in games])

  for comp in Completion:
    filtered_games = [game for game in games if game.completion == comp]

    if(total == 0):
      perc[comp]=0
      continue

    perc[comp] = len(filtered_games) / total

  return {
    "perc":perc
  }

@app.route("/massedit", methods=['POST'])
def mass_edit():
  args = request.form.to_dict()

  # Get all selected IDs
  selected = [] 
  
  for gameid in request.form.getlist('selected'):
    game = db.session.get(GameEntry, gameid)
    if(not game):
      continue
    selected.append(game)

  # Mass apply params
  for game in selected:
    if(args.get("platform")):
      game.platform = args.get("platform")
    if(args.get("completion")):
      game.completion = Completion(int(args.get("completion")))
    if(args.get("priority")):
      game.priority = Priority(int(args.get("priority")))

  db.session.commit()

  flash(f"Modified {len(selected)} games")
  return redirect(request.referrer)

from sqlalchemy import or_

@app.route("/", methods=['GET', 'POST'])
def all_games():
  if request.method == 'POST':

    url_params = request.form.to_dict()
    url_params["priority"] = request.form.getlist("priority")
    url_params["completion"] = request.form.getlist("completion")

    url_params = {k: v for k, v in url_params.items() if v}

    return redirect(url_for("all_games", **url_params))

  args = request.args
  filters = []

  if("platform" in args):
    filters.append(args.get("platform") == GameEntry.platform)

  if("priority" in args):
    all_priority = args.getlist("priority")
    for idx, val in enumerate(all_priority):
      all_priority[idx] = Priority(int(all_priority[idx]))
    print(all_priority)
    filters.append(GameEntry.priority.in_(all_priority))

  if("completion" in args):
    all_completion = args.getlist("completion")
    for idx, val in enumerate(all_completion):
      all_completion[idx] = Completion(int(all_completion[idx]))
    print(all_completion)
    filters.append(GameEntry.completion.in_(all_completion))
  
  #really ugly 'get all platforms' method. TODO: Make seperate table
  all_platforms=[plat[0] for plat in db.session.query(GameEntry.platform).distinct()]
  all_games=db.session.query(GameEntry).filter(*filters)

  stats = get_stats(all_games)

  return render_template(
    'list/detail.html',
    all_games=all_games,
    all_platforms=all_platforms,
    stats=stats,
    Completion=Completion,
    Priority=Priority
  )
