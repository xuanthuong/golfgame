# -*- coding: utf-8 -*-
# Description: Main playing game
# By Thuong.Tran
# Date: 21 Aug 2017

from rule import rule
from user import user

class play_game:
  def __init__(self, hole, user_name, game_type="Single"):
    self.hole = hole
    self.user_name = user_name
    self.game_type = game_type

  def get_score(self, actions):
    return len(actions) - 1

  def save_game(self):
    pass

  def start_game(self):
    game_rule = rule(self.hole, self.user_name)
    usr = user(self.user_name)
    levels = usr.get_levels()

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
      if actions[i] == "green":
        action_type = "Approach"
      elif actions[i] == "putting":
        action_type = "Putting"

      if actions[i+1] == "putting":
        to_location = "green"
      else:
        to_location = "Fairway" if actions[i+1] == "second_shot" or actions[i+1] == "third_shot" else actions[i+1]

      shots.append({
        "distance": 222,
        "toLocation": to_location,
        "score": i - 3,
        "action": action_type
      })
    game_data = {
      "Level": levels,
      "Day": "Monday",
      "Shot": shots,
      "HoleScore": score
    }
    self.save_game()
    return game_data