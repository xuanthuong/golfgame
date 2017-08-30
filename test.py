import json
from play_new_game import play_game
from gen_work_history import gen_rand_work_history
# hole = "Par5"
# user_name = "ThuongTran"

# game = play_game(hole, user_name)
# game_data = game.start_game()
# if game_data:
#   # print(json.dumps(game_data), indent=4)
#   print(game_data)

# work_history = gen_rand_work_history((1, 8, 2017), (31, 8, 2017))
# print(work_history)

import datetime as dt
from models.work_history import work_history

wh = work_history("mysql://user1:user123456!@localhost/my_test")

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