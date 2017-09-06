# import json
# from play_new_game import play_game
# from gen_work_history import gen_rand_work_history

# hole = "Par3"
# user_name = 'ThuongTran'

# game = play_game(hole, user_name)
# game_data = game.start_game()
# if game_data:
#   print(game_data)


# from rule import rule
# game_rule = rule("Par3", "ThuongTran")
# print(game_rule.get_normal_transition_prob(1, 0.005))


from models.gmf_cfd import gmf_cfd

DB_URL = "mysql://golf_user:dounets123!@localhost/golfgame"
a = gmf_cfd(DB_URL)
# for item in a.get_all():
#   print(item.CFD_ID)

# print(a.sp_test_1(359))
for ar in a.get_level('A', 1.6, '2017-09-06 09:00:00'):
  print(ar.LVL_NO)

