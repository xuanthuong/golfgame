# -*- coding: utf-8 -*-
# Description: Service to call data models
# By Thuong.Tran
# Date: 21 Aug 2017

from pymongo import MongoClient
from user_level_model import  user_level
import random

client = MongoClient('localhost', 27017)
db = client.golfgame
user_levels_collection = db.user_levels

def update_levels(user):
  return user.upsert_to(user_levels_collection)

def get_levels(user_name):
  return user_level.get_levels(user_levels_collection, user_name)