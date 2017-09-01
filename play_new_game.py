# -*- coding: utf-8 -*-
# Description: Main playing game
# By Thuong.Tran
# Date: 21 Aug 2017

import datetime as dt
from rule import rule
from golf_distance import golf_distance
from models.hole_history import hole_history
from models.hole import hole
from models.worker_level import worker_level
from models.worker import worker
import random as rd

# DB_URL = os.environ['GOLF_GAME_DB_URL']
# DB_URL = "mysql://golf_user:dounets123!@localhost/golfgame"
DB_URL = "mysql://sql12192591:WDmK2WmCNq@sql12.freemysqlhosting.net/sql12192591"

week_day = {
  '0': 'Mon',
  '1': 'Tue',
  '2': 'Wed',
  '3': 'Thu',
  '4': 'Fri',
  '5': 'Sat',
  '6': 'Sun'  
}

class play_game:
  def __init__(self, hole, user_name, game_type="Single"):
    self.hole = hole
    self.user_name = user_name
    self.game_type = game_type
    wk = worker(DB_URL)
    self.user_id = wk.get_by_username(self.user_name)
    if not self.user_id:
      raise ValueError("This user is not available...")

  def get_score(self, actions):
    return len(actions) - 1

  def save_game(self, game_data):
    hole_hist = hole_history(DB_URL)

    hol = hole(DB_URL)

    hole_data = {
      'PLER_ID': 1,
      'HOLE_TP': self.hole,
      'HOLE_DT': dt.datetime.today(),
      'WK_DY': week_day[str(dt.datetime.today().weekday())],
      'GRP_TP': "N",
      'WRKR_1_ID': 1,
      'WRKR_2_ID': 2,
      'SCRE_NO': game_data['HoleScore']
    }
    hole_id = hol.insert_to(hole_data)

    result_hist = []
    i = 1
    for shot in game_data['Shot']:
      result_hist.append({
        'HOLE_ID': hole_id,
        'CLSS_NO': 1,
        'ORD_NO': i,
        'ACTR_ID': self.user_id,
        'ACT_NM': shot['action'],
        'RSLT_NM': shot['toLocation'],
        'ACT_SCRE': shot['score'],
        'DIST_NO': shot['distance']
      })
      i += 1
    for rec in result_hist:
      hole_hist.insert_to(rec)
    return result_hist


  def start_game(self):
    game_rule = rule(self.hole, self.user_name)

    wkl = worker_level(DB_URL)
    levels = wkl.get_by_id(self.user_id)

    distance_rule = golf_distance(self.hole)

    actions = []
    start_action = game_rule.get_start_action()
    actions.append(start_action)
    cur_action = start_action
    next_action = ""
    while next_action != "inhole":
      next_action = game_rule.get_next_action(levels, cur_action)
      actions.append(next_action)
      cur_action = next_action
    # Finish a hole
    score = self.get_score(actions)
    shots = []
    for i in range(len(actions) - 1):
      action_type = "Driving"
      if actions[i] == "approach":
        action_type = "Approach"
      elif actions[i] == "putting":
        action_type = "Putting"

      if actions[i+1] == "putting" or actions[i+1] == 'approach':
        to_location = "green"
      else:
        to_location = "Fairway" if actions[i+1] == "second_shot" or actions[i+1] == "third_shot" else actions[i+1]

      dist = distance_rule.get_distance(actions[i], actions[i+1])

      shots.append({
        "distance": dist,
        "toLocation": to_location,
        "score": 1,
        "action": action_type
      })

    game_data = {
      "Level": levels,
      "Day": "Monday",
      "Shot": shots,
      "HoleScore": score
    }
    self.save_game(game_data)
    return game_data