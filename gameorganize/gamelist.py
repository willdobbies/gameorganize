from flask import Blueprint, render_template, request, url_for, redirect, flash
from .model.game import GameEntry, Completion, Priority
from .db import db

gamelist = Blueprint('gamelist', __name__, template_folder='templates')

def get_stats(games):
  stats = {}

  total = len([game for game in games])

  for comp in Completion:
    if(comp is Completion.Null):
      continue

    filtered_games = [game for game in games if game.completion == comp]

    if(total == 0):
      stats[comp]=0
      continue

    stats[comp] = int((len(filtered_games) / total)*100)

  return stats

@gamelist.route("/edit", methods=['POST'])
def edit():
  args = request.form.to_dict()

  # Get all selected IDs
  selected = [] 
  
  for gameid in request.form.getlist('selected'):
    game = db.session.get(GameEntry, gameid)
    if(not game):
      continue
    selected.append(game)

  action = request.args.get("action", "modify")

  # Mass apply params
  for game in selected:
    if(action == "delete"):
      db.session.delete(game)
    else:
      if(args.get("platform")):
        game.platform = args.get("platform")
      if(args.get("completion")):
        game.completion = Completion(int(args.get("completion")))
      if(args.get("priority")):
        game.priority = Priority(int(args.get("priority")))

  db.session.commit()

  flash(f"{action} {len(selected)} games")
  return redirect(request.referrer)

@gamelist.route("/", methods=['GET', 'POST'])
def detail():
  if request.method == 'POST':

    url_params = request.form.to_dict()
    url_params["priority"] = request.form.getlist("priority")
    url_params["completion"] = request.form.getlist("completion")
    url_params["platform"] = request.form.getlist("platform")

    url_params = {k: v for k, v in url_params.items() if v}

    return redirect(url_for("gamelist.detail", **url_params))

  args = request.args
  filters = []

  if("platform" in args):
    all_platform = args.getlist("platform")
    filters.append(GameEntry.platform.in_(all_platform))

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
    'gamelist/detail.html',
    all_games=all_games,
    all_platforms=all_platforms,
    stats=stats,
    Completion=Completion,
    Priority=Priority
  )