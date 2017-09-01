import json
from play_new_game import play_game
from gen_work_history import gen_rand_work_history

hole = "Par3"
user_name = 'ThuongTran'

game = play_game(hole, user_name)
game_data = game.start_game()
if game_data:
  print(game_data)


# from rule import rule
# game_rule = rule("Par3", "ThuongTran")
# print(game_rule.get_normal_transition_prob(1, 0.005))