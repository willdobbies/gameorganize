from .db import db
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform, get_user_platforms
from .model.user import User
from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
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

@user.route("/platforms", methods=['GET', 'POST'])
def platform_list(username):
  _user = db.session.query(User).where(User.username==username).first()
  return render_template(
    'user/platforms.html',
    username=_user.username,
    platforms=_user.platforms,
  )

@user.route("/platforms/add", methods=['POST'])
@login_required
def platform_add():
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
    return redirect(url_for('user.platform_list', username=current_user.username))

  flash(f"Added new platform {new_platform.name}")
  return redirect(url_for('user.platform_list', username=current_user.username))

@user.route("/platforms/<id>/delete", methods=['POST'])
@login_required
def platform_delete(id):
  platform = db.session.get(Platform, id)

  if(not platform):
    abort(404)

  if(platform.user_id != current_user.id):
    abort(403)
  
  db.session.delete(platform)
  db.session.commit()

  flash(f"Deleted platform {platform.name}")
  return redirect(url_for('user.platform_list', username=current_user.username))

@user.route("/edit", methods=['POST'])
@login_required
def edit(username):
  _user = db.session.query(User).where(User.username==username).first()

  if(_user.id != current_user.id):
    abort(403)

  # Get game selection
  args = request.form.to_dict()
  selected = [] 
  
  for gameid in request.form.getlist('selected'):
    game = db.session.get(GameEntry, gameid)
    if(not game):
      continue

    if(game.user_id != current_user.id):
      abort(403)

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

  flash(f"Ran {action} on {len(selected)} games")
  return redirect(url_for("user.detail", username=current_user.username))

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

  return filters,filter_parse

@user.route("/", methods=['POST'])
def detail_post(username):
    url_params = request.form.to_dict()
    url_params["priority"] = request.form.getlist("priority")
    url_params["completion"] = request.form.getlist("completion")
    url_params["platform_id"] = request.form.getlist("platform_id")

    url_params = {k: v for k, v in url_params.items() if v}

    return redirect(url_for("user.detail", username=username, **url_params))

@user.route("/", methods=['GET'])
def detail(username):
  user = db.session.query(User).where(User.username==username).first()
  if(not user):
    abort(404)
  
  # Improve this, add pagination?
  filters,filter_parse = parse_filters(request.args)
  games = db.session.query(GameEntry).where(GameEntry.user_id==user.id)
  if(games):
    games = games.filter(*filters)

  return render_template(
    'user/detail.html',
    filter=filter_parse,
    Completion=Completion,
    Priority=Priority,
    games=games,
    platforms=user.platforms,
    stats=get_stats(games),
    username=username,
  )