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
# from models.worker_level import worker_level
# import datetime as dt
# import random as rd

# DB_URL = "mysql://golf_user:dounets123!@localhost/golfgame"
# DB_URL = "mysql://gamification:123789@10.0.14.199/gamification-fwd"
# print(DB_URL)
# DB_URL = "mysql://sql12192591:WDmK2WmCNq@sql12.freemysqlhosting.net/sql12192591"

# wk = worker(DB_URL)
# users = ['thuongtran', 'vanngo', 'khangdong', 'lucduong']
# for user in users:
#   wk.insert_to({
#     'WRKR_NM': user,
#     'CRE_DT': dt.datetime.today()
#   })

# wkl = worker_level(DB_URL)
# for i in range(4):
#   temp = {
#     'CFD_ID': 1,
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

# print(wkl.get_by_id(1))

