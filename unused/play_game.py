# -*- coding: utf-8 -*-
# Test play simple golf game for one user
# Game - example scenario
# Một ngày user hoàn thành bao nhiêu process không quan trọng, nó cứ cập nhật vào round-robin list thôi
# Dù không hoàn thành process thì cũng ko sao (vẫn dùng dữ liệu r-r gần nhất trước đó), 
# nhưng ngày hôm sau level sẽ xuống thấp -> dẫn đến khả năng thắng game sẽ giảm đi

# Dữ liệu ban đầu gồm có: 
# 	round-robin -> của user
# 	cfd table -> của việc tính toán từ tất cả các process của tất cả user trong 1 tháng gần nhất

import random
import json

TRANSITION_PROB = {
  "Par3": {
    "driving_shot": {
      "approach": 0.5,
      "bunker": 0.495,
      "water": 0.495,
      "ruff": 0.495,
      "end": 0.005,
    },
    "approach": {
      "approach": 0.49,
      "bunker": 0.49,
      "water": 0.49,
      "ruff": 0.49,
      "putting": 0.5,
      "end": 0.01,
    },
    "putting": {
      "putting": 0.5,
      "end": 0.5,
      "bunker": 0.5,
      "ruff": 0.5,
    },
    "water": {
      "approach": 0.9,
      "ruff": 0.1,
    },
    "bunker": {
      "bunker": 0.5,
      "approach": 0.5,
      "ruff": 0.5,
    },
    "ruff": {
      "ruff": 0.5,
      "bunker": 0.5,
      "approach": 0.5,
    }
  },
  "Par4": "undefined"
}

# 
def get_round_robin(user_name):
  return [8, 10, 7, 1, 0, 6, 0, 3, 9, 10]

def retrieve_cfd_table():
  table = "call api or select into database"
  return table
# ################

# class Rule
def get_start_action():
  return "driving_shot"

def get_possible_next_actions(hole, cur_action):
  return TRANSITION_PROB[hole][cur_action]

def get_next_normal_action(hole, levels, cur_action):
  lists_next_actions = get_possible_next_actions(hole, cur_action)
  prob_arr = []
  for action, expect_prob in lists_next_actions.items():
    prob = get_transition_prob_by_levels(levels, expect_prob)
    prob_arr.append((action, prob))

  next_action = max(prob_arr, key=lambda x:x[1])
  return next_action

# Transition probability -> fix or have to recalculate???
def get_normal_transition_prob(level, expect_prob):
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

def get_transition_prob_by_levels(levels, expect_prob):
  tmp_arr = [get_normal_transition_prob(level, expect_prob) for level in levels]
  return sum(tmp_arr)/len(tmp_arr)


# #################
def get_next_action(hole, levels, cur_action):
  lists_next_actions = get_possible_next_actions(hole, cur_action)

  next_normal_action = get_next_normal_action(hole, levels, cur_action)
  action_name = next_normal_action[0]
  prob = next_normal_action[1]
  
  # return action_name

  lucky_rnd = random.random()
  if lucky_rnd <= prob:
    return action_name
  else:
    lucky_rnd = 1 - lucky_rnd
    sum_R1 = 0
    sum_R2 = 0
    for action, expect_prob in lists_next_actions.items():
      if action != action_name:
        tmp = get_transition_prob_by_levels(levels, expect_prob)
        sum_R2 = sum_R1
        sum_R1 += tmp
        if sum_R2 <= lucky_rnd < sum_R1:
          return action
  return action_name


# #################

# 
def get_score(actions):
  return len(actions)

def save_game():
  pass
# #################

# Start game
def start_game(user_name):
  levels = get_round_robin(user_name)
  actions = []
  start_action = get_start_action()
  actions.append(start_action)
  cur_action = start_action
  next_action = ""
  while next_action != "end":
    next_action = get_next_action("Par3", levels, cur_action)
    actions.append(next_action)
    cur_action = next_action
    # print("current action: %s" % cur_action)

  score = get_score(actions)
  # print(actions)

  shots = []
  for i in range(len(actions) - 1):
    shots.append({
      "from": actions[i],
      "to": actions[i+1],
      "score": i - 3
    })
  game_data = {
    "Level": levels,
    "Day": "Monday",
    "Shot": shots,
    "TotalScore": score
  }
  save_game()
  # print(json.dumps(game_data, indent=4))
  return game_data

  
if __name__ == "__main__":
  start_game("ThuongTran")

  # # Test get round-robin list
  # levels = get_round_robin("ThuongTran")
  # print("levels: %s of ThuongTran:" % levels)

  # # Test get possible next actions
  # next_actions = get_possible_next_actions("Par3", "driving_shot")
  # print(next_actions)

  # # Test get transition possibility
  # # print(get_transition_prob(5,2,3))
 
  # # Test get next normal action
  # next_normal_action = get_next_normal_action("Par3", levels, "driving_shot")
  # print("next normal action with prob: ", next_normal_action)

  # # Test get next game action
  # next_game_action = get_next_action("Par3", levels, "driving_shot")
  # print("next game action with prob: ", next_game_action)




# Show game
# Monday: 2 tasks completed - 0 task remain
# Print
# 		Gậy 1: from ... to ...
# 		Gậy 2: from ... to ...
# 		Gậy 3: from ... to ...
# 		Par
# Tuesday: 3 tasks completed - 0 task remain
# 		Gậy 1: from ... to ...
# 		Gậy 2: from ... to ...
# 		Gậy 3: from ... to ...
# 		Gậy 4: from ... to ...
# 		Par
# Wednesday: 0 task completed - 2 tasks remain
# 		Gậy 1: from ... to ...
# 		Gậy 2: from ... to ...
# 		Gậy 3: from ... to ...
# 		Gậy 4: from ... to ...
# 		Gậy 5: from ... to ...
# 		Double
# Thursday: 1 task completed - 1 task remain
# 		...
# Friday: 2 tasks completed - 0 task remain
# 		...
# -> Sunday -> result score