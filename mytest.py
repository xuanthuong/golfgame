# import os
# import json
# from play_new_game import play_game
# from gen_work_history import gen_rand_work_history


# hole = "Par3"
# user_name = "ThuongTran"

# game = play_game(hole, user_name)
# game_data = game.start_game()
# if game_data:
#   # print(json.dumps(game_data), indent=4)
#   print(game_data)

##############################
# work_history = gen_rand_work_history((1, 8, 2017), (31, 8, 2017))
# print(work_history)

# import datetime as dt
# from models.work_history import work_history

# wh = work_history("mysql://user1:user123456!@localhost/my_test")

# today = dt.datetime.today()
# data = {
#       'USR_ID': 1,
#       'PROC_NM': 'A',
#       'ST_DT': today,
#       'END_DT': today,
#       'LD_TM': 0.45,
#       'CRE_DT': today
#     }
# wh.insert_to(data)
# result = wh.get_all()
# print(json.dumps(result))
# # for r in result:
# #   # print(r['ST_DT'])
# #   # print(r['PROC_NM'])
# #   print


# # Mongo test
# from pymongo import MongoClient
# from user_level_model import  user_level
# import random

# client = MongoClient('localhost', 27017)
# db = client.golfgame

# user_levels_collection = db.user_levels

# user = user_level('ThuongTran', [random.randint(1,11) for r in range(10)])
# inserted_id = user.upsert_to(user_levels_collection)
# print('Inserted: ', inserted_id)

# user1 = user_level('VanNgo', [random.randint(1,11) for r in xrange(10)])
# user2 = user_level('KhangDong',[random.randint(1,11) for r in xrange(10)])
# user3 = user_level('LucDuong', [random.randint(1,11) for r in xrange(10)])
# inserted_ids = user_level.bulk_insert(user_levels_collection, [user1, user2, user3]) # Staticmethod
# print ('Inserted Ids: ', inserted_ids)

# # 2nd Mongo test
# from models_service import get_levels
# from user_level_model import user_level
# import random

# user = user_level('ThuongTran', [random.randint(1,11) for r in range(10)])
# print(get_levels(user))


# # Insert some users to db
# from models.worker import worker
from models.worker_level import worker_level
import datetime as dt
import random as rd
from models.game import game
from models.league import league
from models.player import player

DB_URL = "mysql://golf_user:dounets123!@localhost/golfgame"
# DB_URL = "mysql://gamification:123789@10.0.14.199/gamification-fwd"
# print(DB_URL)
# DB_URL = "mysql://sql12192591:WDmK2WmCNq@sql12.freemysqlhosting.net/sql12192591"

# ############# Insert data to worker table
# wk = worker(DB_URL)
# users = ['thuongtran', 'vanngo', 'khangdong', 'lucduong']
# for user in users:
#   wk.insert_to({
#     'WRKR_NM': user,
#     'CRE_DT': dt.datetime.today()
#   })

# ############# Insert data to worker level
# wkl = worker_level(DB_URL)
# for i in range(4):
#   temp = {
#     'CFD_ID': 2,
#     'WRKR_ID': i + 1,
#     'LVL_1_NO': rd.randint(1, 10),
#     'LVL_2_NO': rd.randint(1, 10),
#     'LVL_3_NO': rd.randint(1, 10),
#     'LVL_4_NO': rd.randint(1, 10),
#     'LVL_5_NO': rd.randint(1, 10),
#     'LVL_6_NO': rd.randint(1, 10),
#     'LVL_7_NO': rd.randint(1, 10),
#     'LVL_8_NO': rd.randint(1, 10),
#     'LVL_9_NO': rd.randint(1, 10),
#     'LVL_10_NO': rd.randint(1, 10)
#   }
#   wkl.insert_to(temp)


# # ############ Insert data to game
# gm = game(DB_URL)
# for i in range(1, 11):
#   temp = {
#     "GAME_NM": "AUG 2th Week",
#     "GAME_TP": "GF",
#     "ST_DT": dt.date(2017, 8, 21),
#     "END_DT": dt.date(2017, 8, 25),
#     "LEAG_ID": 1,
#     "PLY_TP": "STK",
#     "WINR_TP": "S",
#     "CFD_ID": 1
#   }
#   print(gm.insert_to(temp))

# # ############ Insert data to League
# lg = league(DB_URL)
# temp = {
#   "LEAG_NM": "2017 CLT CHAMPION",
# }
# print(lg.insert_to(temp))

# # ############ Insert data to Player
# pl = player(DB_URL)
# for i in range(1, 11):
#   temp = {
#     "GAME_ID": i,
#     "PLER_TP": "S",
#     "SCRE_NO": rd.randint(3,20),
#     "GRD_NO": 1,
#     "TEAM_ID": 1
#   }
#   print(pl.insert_to(temp))

# # ########### Test call procedure to get game results
# from models.sqlprocedure import sqlprocedure
# sql_proc = sqlprocedure(DB_URL)

# params = {
#   'league_name': '2017 CLT CHAMPION',
#   'start_date': '2017-08-14',
#   'end_date': '2017-08-18',
#   'worker_id': 1
# }
# result = sql_proc.get_game_results(params)
# print(result[0]['HOLE_TP'])

# test_obj = {
  #     'IDX': 8,
  #     'CFD_ID': 2,
  #     'WRKR_ID': 1,
  #     'LVL_1_NO': 1,
  #     'LVL_2_NO': 8,
  #     'LVL_3_NO': 3,
  #     'LVL_4_NO': 3,
  #     'LVL_5_NO': 8,
  #     'LVL_6_NO': 4,
  #     'LVL_7_NO': 4,
  #     'LVL_8_NO': 4,
  #     'LVL_9_NO': 5,
  #     'LVL_10_NO': 5
  #   }
  # wk_level.update(8, test_obj)

# ######### Test update levels#
# today = dt.datetime(2017, 8, 28)
# update_levels(today, 1)
# print(wk_level.get_by_id(4))


# # ####### Test playing game
# hole = "Par3"
# user_name = 'ThuongTran'

# game = play_game(hole, user_name)
# game_data = game.start_game()
# if game_data:
#   print(game_data)


# from rule import rule
# game_rule = rule("Par3", "ThuongTran")
# print(game_rule.get_normal_transition_prob(1, 0.005))

# import datetime as dt
# from models.gmf_cfd import gmf_cfd
# from models.work_history import work_history

# DB_URL = "mysql://golf_user:dounets123!@localhost/golfgame"
# a = gmf_cfd(DB_URL)
# work_his = work_history(DB_URL)
# for item in a.get_all():
#   print(item.CFD_ID)

# Test get cfd_id and level from CFD table
# print(a.sp_test_1(359))
# for ar in a.get_level('A', 1.6, '2017-07-31 17:00:00', '2017-08-30 17:00:00'):
#   print(ar.LVL_NO)

# for arr in a.get_by_period('2017-07-31 17:00:00', '2017-08-30 17:00:00'):
#   print(arr['LVL_NO'])


# today = dt.datetime.today()
# start_date = today - dt.timedelta(days=30)
# for r in work_his.get_by_period(start_date, today):
#   print(r)