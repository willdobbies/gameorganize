from .db import db
from .importers.retroachievements import ImporterRA
from .importers.steam import ImporterSteam
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform, find_platform
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
import csv

importer = Blueprint('importer', __name__, template_folder='templates')

#def add_or_update_game(new_game):
#  try:
#    # check if game name already exists
#    dupe_game = db.session.query(GameEntry).filter_by(name="Hi").first()
#
#    # update old entry if exists
#    if(dupe_game):
#      new_game.id = dupe_game.id
#      dupe_game = new_game
#    else:
#      db.session.add(new_game)
#
#    db.session.commit()
#  except Exception as e:
#    flash(f"DB Errorr: {e}")
#    return False
#  return True

#def import_steam(id, key):
#  importer = ImporterSteam(id, key)
#  fdata = importer.fetch()
#  return importer.parse(fdata)
#
#def import_ra(id, key):
#  importer = ImporterRA(username=id, api_key=key)
#  fdata = importer.fetch()
#  return importer.parse(fdata)

def find_or_create_platform(user, platform_name):
  platform = db.session.query(Platform).filter_by(name=platform_name).first()

  if(platform):
    return platform
  
  try:
    new_platform = Platform(
      name = platform_name,
      user = user
    )

    db.session.add(platform)
    db.session.commit()

  except Exception as e:
    db.session.rollback()
    flash(f"DB Error: {e}")
    return None

  return new_platform

def parse_csv_line(line, user):
  platform_name = line.get("Platform")
  platform = find_or_create_platform(user, platform_name)

  try:
    new_game = GameEntry(
      name = line.get("Name"),
      platform = platform,
      completion = Completion[line.get("Completion")],
      priority = Priority[line.get("Priority")],
      notes = line.get("Notes"),
    )

    db.session.add(new_game)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    flash(f"DB Error: {e}")
    return None

  return new_game


def import_csv(csv_raw, user):
  if(not csv_raw):
    flash("Missing CSV data")
    return []
    #redirect(url_for(importer.detail))
    #return []

  csv_parsed = csv_raw.read().decode("utf-8").split("\n")
  csv_reader = csv.DictReader(csv_parsed)

  new_games = []

  for line in csv_reader:
    new_game = parse_csv_line(line, user)
    if(new_game):
      new_games.append(new_game)
  return new_games

@importer.route("/", methods=['POST'])
@login_required
def import_post():
  site = request.form.get("website")
  apiId = request.form.get("id")
  apiKey = request.form.get("key")
  csvdata = request.files.get("csv")

  new_games = []

#  if(site == "Steam"):
#    new_games = import_steam(apiId, apiKey)

#  elif(site == "RetroAchievements"):
#    new_games = import_ra(apiId, apiKey)

  if(site == "CSV"):
    new_games = import_csv(csvdata, current_user)

  flash(f"Imported {len(new_games)} games from {site}")
  return redirect(url_for('importer.detail'))

@importer.route("/", methods=['GET'])
@login_required
def detail():
  return render_template(
    'importer/detail.html'
  )