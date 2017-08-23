# -*- coding: utf-8 -*-
# Description: Define some rules of golf game
# By Thuong.Tran
# Date: 21 Aug 2017

import random
import json

FILE_DIR = "./rule_data.json"

class rule:
  def __init__(self, hole, game_type):
    self.hole = hole
    self.game_type = game_type
    self.transition_prob = self.read_rule_data()

  def read_rule_data(self):
    transition_prob = {}
    with open(FILE_DIR) as rule_data:
      transition_prob = json.load(rule_data)
    return transition_prob

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
      diff = 0.1 if level == 5 else (0.2 if level == 4 else (
              0.3 if level == 3 else (0.4 if level == 2 else (0.5 if level == 1 else 0.0))))
      prob += diff
      prob = 1 if prob > 1.0 else prob
    else:
      diff = 0.1 if level == 10 else (0.2 if level == 9 else (
              0.3 if level == 8 else (0.4 if level == 7 else (0.5 if level == 6 else 0.0))))
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