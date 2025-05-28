from .importers.retroachievements import ImporterRA
from .importers.steam import ImporterSteam
from .importers.generic import import_csv
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

@importer.route("/", methods=['POST'])
@login_required
def import_post():
  site = request.form.get("website")
  apiId = request.form.get("id")
  apiKey = request.form.get("key")
  csv_data = request.files.get("csv_data")

  new_games = []

#  if(site == "Steam"):
#    new_games = import_steam(apiId, apiKey)

#  elif(site == "RetroAchievements"):
#    new_games = import_ra(apiId, apiKey)

  if(site == "CSV"):
    new_games = import_csv(csv_data, current_user)

  flash(f"Imported {len(new_games)} games from {site}")
  return redirect(url_for('importer.detail'))

@importer.route("/", methods=['GET'])
@login_required
def detail():
  return render_template(
    'importer/detail.html'
  )