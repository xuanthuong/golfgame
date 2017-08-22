# import json
# from play_new_game import play_game

# hole = "Par3"
# user_name = "userA"

# game = play_game(hole, user_name)
# game_data = game.start_game()
# if game_data:
#   print(json.dumps(game_data), 200)


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

# 2nd Mongo test
from models_service import get_levels
from user_level_model import user_level
import random

user = user_level('ThuongTran', [random.randint(1,11) for r in range(10)])
print(get_levels(user))