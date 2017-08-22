# -*- coding: utf-8 -*-
# Description: User with levels model
# By Thuong.Tran
# Date: 21 Aug 2017

import datetime
import json
from bson import BSON
from bson import json_util

class user_level:
  def __init__(self, user_name, levels):
    self.user_name = user_name
    self.levels = levels

  def insert_to(self, collection):
      if self.user_name == '' or self.levels == '':
        return False
      else:
        today = datetime.datetime.today()
        user = {
            'user_name': self.user_name,
            'levels': self.levels,
            'created_at': today.strftime('%H:%M:%S %Y-%m-%d')
        }
        return collection.insert_one(user).inserted_id
  

  def upsert_to(self, collection):
      if self.user_name == '' or self.levels == '':
        return False
      else:
        today = datetime.datetime.today()
        user = {
            'user_name': self.user_name,
            'levels': self.levels,
            'created_at': today.strftime('%H:%M:%S %Y-%m-%d')
        }
        upsert_id = collection.update_one({"user_name": self.user_name}, {"$set": user}, upsert=True)
        return upsert_id
  
  @staticmethod
  def get_levels(collection, username):
    user = collection.find_one({"user_name": username})
    if user:
      user = json.dumps(user, indent=4, default=json_util.default)
      return user
    return {}

  @staticmethod
  def bulk_insert(collection, users_list):
    today = datetime.datetime.today()
    users = []
    for user in users_list:
      if user.user_name != '' and user.levels != '':
        user = {
          'user_name': user.user_name,
          'levels': user.levels,
          'created_at': today.strftime('%H:%M:%S %Y-%m-%d')
        }
        users.append(user)
    if len(users) > 0:
      result = collection.insert_many(users)
      return result.inserted_ids
    return []