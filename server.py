import os
import sys
import json

# import requests
from flask import Flask, request, jsonify

from config import get_DB_URL
from play_new_game import play_game
import random as rd
from gen_work_history import gen_rand_work_history
from models.worker_level import worker_level
from models.worker import worker
from models.work_history import work_history
from models.game import game
from models.ranking import rank
from notify_hole_results import get_hole_results, get_hole_details
import datetime as dt
from notify_game_results import notify_game_results


app = Flask(__name__)

DB_URL = get_DB_URL()
print("DB URL at server.py: %s" % DB_URL)

@app.route('/', methods=['GET'])
def verify():
  # when the endpoint is registered as a webhook, it must echo back
  # the 'hub.challenge' value it receives in the query arguments
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200

  return "This web server contains APIs for gamification", 200


@app.route('/golfgame-api/getlevels', methods=['GET'])
def webhook1():
  params = request.json
  print(params)
  if 'username' in params:
    user_name = params['username']
    if user_name != "All":
      wk = worker(DB_URL)
      wkl = worker_level(DB_URL)
      user_id = wk.get_by_username(user_name)
      levels = wkl.get_by_id(user_id)
      print(levels)
      return jsonify({"username": user_name, "levels": levels}), 200
    else:
      return "No username", 200
  else:
    return "No params", 200

@app.route('/golfgame-api/playgame', methods=['POST'])
def webhook():
  params = request.json
  hole = params['hole']
  user_name = params['username']

  if user_name != "All":
    game = play_game(hole, user_name)
    game_data = game.start_game()
    if game_data:
      return jsonify(game_data), 200 
    else:
      return "No game data", 200
  else:
    return "No username", 200

  return "OK", 200


@app.route('/golfgame-api/work-history', methods=['GET'])
def rand_work_history():
  work_history = gen_rand_work_history((1, 8, 2017), (31, 8, 2017))
  return jsonify(work_history), 200


@app.route('/golfgame-api/work-history', methods=['POST'])
def insert_work_history():
  params = request.json
  work = {
    'USR_ID': params['USR_ID'],
    'PROC_NM': params['PROC_NM'],
    'ST_DT': dt.datetime.strptime(params['ST_DT'], "%b %d, %Y %H:%M:%S"),
    'END_DT': dt.datetime.strptime(params['END_DT'], "%b %d, %Y %H:%M:%S"),
    'LD_TM': params['LD_TM'],
    'CRE_DT': dt.datetime.today()
    }

  for usr in work['USR_ID']:
    tmp = work
    wk = worker(DB_URL)
    wrk_hist = work_history(DB_URL)
    tmp['USR_ID'] = wk.get_by_username(usr)
    wrk_hist.insert_to(tmp)

  return "ok", 200

@app.route('/golfgame-api/notify-hole-results', methods=['POST'])
def notify_hole_results():
  params = request.json
  user_name = params['username']
  leage_name = params['leagename']
  start_date = dt.date(2017, 9, 11)
  end_date = dt.date(2017, 9, 15)
  wk = worker(DB_URL)
  worker_id = wk.get_by_username(user_name)
  parse_params = {
    'league_name': leage_name,
    'start_date': dt.date(2017, 9, 11),
    'end_date': dt.date(2017, 9, 15),
    'worker_id': worker_id
  }
  res = get_hole_results(parse_params)
  if res:
    return jsonify(res), 200
  else:
    return "No data found", 200


@app.route('/golfgame-api/notify-hole-details', methods=['POST'])
def notify_hole_details():
  params = request.json
  hole_id = params['holeId']

  if hole_id:
    res = get_hole_details(hole_id)
    if res:
      return jsonify(res), 200
    else:
      return "No data found", 200
  else:
    return "No hole id received", 200


@app.route('/golfgame-api/notify-game-results', methods=['POST'])
def notify_game_results_api():
  params = request.json  
  user_name = params['username']
  leage_name = params['leagename']
  start_date = dt.date(2017, 9, 11)
  end_date = dt.date(2017, 9, 15)
  wk = worker(DB_URL)
  worker_id = wk.get_by_username(user_name)

  if user_name:
    gm_result = notify_game_results(leage_name, start_date, end_date)
    game_results = gm_result.call_cal_game_results(gm_result, worker_id)

  else:
    return "No user name", 200
  return jsonify(game_results), 200

@app.route('/golfgame-api/notify-game-ranking', methods=['POST'])
def notify_ranking():
  params = request.json  
  user_name = params['username']
  leage_name = params['leagename']
  start_date = dt.date(2017, 9, 11)
  end_date = dt.date(2017, 9, 15)

  if user_name:
    rnk = rank(DB_URL)
    ranking_obj = rnk.get_all()
    rank_results = []
    for r in ranking_obj:
      rank_results.append({
        'rank': r['RNK_NO'],
        'player': r['WRKR_NM'],
        'point': r['PNT_NO']
      })
    return jsonify(rank_results), 200

  else:
    return "No user name", 200


def log(message):  # simple wrapper for logging to stdout on heroku
  print(message)
  sys.stdout.flush()


if __name__ == '__main__':
  # app.run(debug=True, host="0.0.0.0", port=5055)
  app.run(debug=True, host="0.0.0.0")
  