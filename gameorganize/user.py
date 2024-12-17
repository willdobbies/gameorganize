from .db import db
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform, get_user_platforms
from .model.user import User
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user

user = Blueprint('user', __name__, template_folder='templates')

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

@user.route("/<username>/platforms", methods=['GET', 'POST'])
@login_required
def platform_list(username):
  _user = db.session.query(User).where(User.username==username).first()
  return render_template(
    'user/platforms.html',
    username=_user.username,
    platforms=_user.platforms,
  )

@user.route("/<username>/platforms/add", methods=['POST'])
@login_required
def platform_add(username):
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
    return redirect(url_for('user.platform_list', username=username))

  flash(f"Added new platform {new_platform.name}")
  return redirect(url_for('user.platform_list', username=username))

@user.route("/<username>/platforms/<id>/delete", methods=['POST'])
@login_required
def platform_delete(username, id):
  _user = db.session.query(User).where(User.username==username).first()
  platform = db.session.query(Platform).where(Platform.id==id, Platform.user_id==_user.id).first()

  if(not platform):
    flash(f"Error: Platform ID {id} not found")
    return redirect(url_for('user.platform_list', username=username))
  
  db.session.delete(platform)
  db.session.commit()

  flash(f"Deleted platform {platform.name}")
  return redirect(url_for('user.platform_list', username=username))

@user.route("/<username>/edit", methods=['POST'])
@login_required
def edit(username):
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
        game.platform_id = args.get("platform")
      if(args.get("completion")):
        game.completion = Completion(int(args.get("completion")))
      if(args.get("priority")):
        game.priority = Priority(int(args.get("priority")))

  db.session.commit()

  flash(f"{action} {len(selected)} games")
  return redirect(request.referrer)

def parse_filters(args):
  filters = []
  filter_parse = {}

  # Convert values back to objects
  filter_parse["platform_id"] = args.getlist("platform_id")
  for idx, val in enumerate(filter_parse["platform_id"]):
    filter_parse["platform_id"][idx] = int(val)

  filter_parse["priority"] = args.getlist("priority")
  for idx, val in enumerate(filter_parse["priority"]):
    filter_parse["priority"][idx] = Priority(int(val))

  filter_parse["completion"] = args.getlist("completion")
  for idx, val in enumerate(filter_parse["completion"]):
    filter_parse["completion"][idx] = Completion(int(val))

  # Apply filters to GameEntry query
  if("platform_id" in args):
    filters.append(GameEntry.platform_id.in_(filter_parse["platform_id"]))

  if("priority" in args):
    filters.append(GameEntry.priority.in_(filter_parse["priority"]))

  if("completion" in args):
    filters.append(GameEntry.completion.in_(filter_parse["completion"]))

  #filters.append(GameEntry.user_id==id)
  return filters,filter_parse

@user.route("/<username>", methods=['GET', 'POST'])
def detail(username):
  _user = db.session.query(User).where(User.username==username).first()
  
  if request.method == 'POST':

    url_params = request.form.to_dict()
    url_params["priority"] = request.form.getlist("priority")
    url_params["completion"] = request.form.getlist("completion")
    url_params["platform_id"] = request.form.getlist("platform_id")

    url_params = {k: v for k, v in url_params.items() if v}

    return redirect(url_for("user.detail", username=username, **url_params))

  filters,filter_parse = parse_filters(request.args)
  games = db.session.query(GameEntry).where(GameEntry.user_id==_user.id)
  if(games):
    games = games.filter(*filters)

  return render_template(
    'user/detail.html',
    filter=filter_parse,
    Completion=Completion,
    Priority=Priority,
    games=games,
    platforms=_user.platforms,
    stats=get_stats(games),
    username=username,
  )