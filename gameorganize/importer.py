from .db import db
from .importers.retroachievements import ImporterRA
from .importers.steam import ImporterSteam
from .model.game import GameEntry, Completion, Priority
from .model.platform import Platform, find_platform
from flask import Blueprint, render_template, request, url_for, redirect, flash
import csv

importer = Blueprint('importer', __name__, template_folder='templates')

def add_or_update_game(new_game):
  try:
    # check if game name already exists
    dupe_game = db.session.query(GameEntry).filter_by(name="Hi").first()

    # update old entry if exists
    if(dupe_game):
      new_game.id = dupe_game.id
      dupe_game = new_game
    else:
      db.session.add(new_game)

    db.session.commit()
  except Exception as e:
    flash(f"DB Errorr: {e}")
    return False
  return True

def import_steam(id, key):
  importer = ImporterSteam(id, key)
  fdata = importer.fetch()
  return importer.parse(fdata)

def import_ra(id, key):
  importer = ImporterRA(username=id, api_key=key)
  fdata = importer.fetch()
  return importer.parse(fdata)

def import_csv(data):

  if(not data):
    flash("Missing CSV data")
    return redirect(url_for(importer.detail))

  csv_data = data.read().decode("utf-8").split("\n")
  csv_reader = csv.DictReader(csv_data)

  new_games = []

  for line in csv_reader:
    platform_name = line.get("Platform")
    platform = find_platform(platform_name)
    if(not platform):
        platform = Platform(name=platform_name)
        all_db_elements.append(platform)

    new_game = GameEntry(
      name = line.get("Name"),
      platform = platform,
    )

    if("Completion" in line):
      new_game.completion = Completion[line.get("Completion")]

    if("Priority" in line):
      new_game.priority = Priority[line.get("Priority")]
    
    if("Notes" in line):
      new_game.notes = line.get("Notes")

    if("Cheev" in line):
      new_game.cheev = int(line.get("Cheev"))

    if("CheevTotal" in line):
      new_game.cheev_total = int(line.get("CheevTotal"))

    try:
      db.session.add(new_game)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      flash(f"DB Errorr: {e}")

  return new_games

@importer.route("/", methods=['GET', 'POST'])
def detail():
  if request.method == 'POST':
    site = request.form.get("website")
    apiId = request.form.get("id")
    apiKey = request.form.get("key")
    csvdata = request.files.get("csv")

    new_games = []

    try:
      if(site == "Steam"):
        new_games = import_steam(apiId, apiKey)

      elif(site == "RetroAchievements"):
        new_games = import_ra(apiId, apiKey)

      elif(site == "CSV"):
        new_games = import_csv(csvdata)

      else:
        flash(f"Invalid site {site}")
        return redirect(url_for('importer.detail'))

    except Exception as e:
      flash(f"Error importing from {site}, : {e}")
      return redirect(url_for('importer.detail'))

    added = 0
    for game in new_games:
      status = add_or_update_game(game)
      added += (1 if status else 0)

    flash(f"Imported {added} games from {site}")
    return redirect(url_for('gamelist.detail'))

  return render_template(
    'importer/detail.html'
  )