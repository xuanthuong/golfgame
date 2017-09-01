# -*- coding: utf-8 -*-
# Description: Define some rules of golf game
# By Thuong.Tran
# Date: 21 Aug 2017

import random
import json

RULE_DATA = "./data/rule_data.json"
LEVEL_PROB = "./data/level_prob.json"

class rule:
  def __init__(self, hole, game_type):
    self.hole = hole
    self.game_type = game_type
    self.transition_prob = self.read_json(RULE_DATA)
    self.level_prob = self.read_json(LEVEL_PROB)

  def read_json(self, DIR):
    result= {}
    with open(DIR) as data:
      result = json.load(data)
    return result

  def get_start_action(self):
    return "driving_shot"

  def get_possible_next_actions(self, cur_action):
    return self.transition_prob[self.hole][cur_action]

  def get_next_normal_action(self, levels, cur_action):
    lists_next_actions = self.get_possible_next_actions(cur_action)
    prob_arr = []
    for action, expect_prob in lists_next_actions.items():
      prob = self.get_transition_prob_by_levels(levels, expect_prob)
      prob_arr.append((action, prob))

    next_action = max(prob_arr, key=lambda x:x[1])
    return next_action

  # Transition probability -> fix or have to recalculate???
  def get_normal_transition_prob(self, level, expect_prob):
    prob = expect_prob
    if (level <= 5):
      diff = self.level_prob["level<=5"][str(level)] if str(level) in self.level_prob["level<=5"] else 0
      prob += diff
      prob = 1 if prob > 1.0 else prob
    else:
      diff = self.level_prob["level>5"][str(level)] if str(level) in self.level_prob["level>5"] else 0
      prob -= diff
      prob = 0.0 if prob < 0.0 else prob
    return prob

  def get_transition_prob_by_levels(self, levels, expect_prob):
    tmp_arr = [self.get_normal_transition_prob(level, expect_prob) for level in levels]
    return sum(tmp_arr)/len(tmp_arr)

  def get_next_action(self, levels, cur_action):
    lists_next_actions = self.get_possible_next_actions(cur_action)

    next_normal_action = self.get_next_normal_action(levels, cur_action)
    action_name = next_normal_action[0]
    prob = next_normal_action[1]

    lucky_rnd = random.random()
    if lucky_rnd <= prob:
      return action_name
    else:
      lucky_rnd = 1 - lucky_rnd
      sum_R1 = 0
      sum_R2 = 0
      for action, expect_prob in lists_next_actions.items():
        if action != action_name:
          tmp = self.get_transition_prob_by_levels(levels, expect_prob)
          sum_R2 = sum_R1
          sum_R1 += tmp
          if sum_R2 <= lucky_rnd < sum_R1:
            return action
    return action_name