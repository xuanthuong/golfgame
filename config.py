# -*- coding: utf-8 -*-
# Description: Configure enviroment vairables
# By Thuong.Tran
# Date: 21 Aug 2017

import os

def get_DB_URL():
  return os.environ['GOLF_GAME_DB_URL']
  # return "mysql://golf_user:123789@gmf-db.dounets.com/gamification"
  # return "mysql://golf_user:dounets123!@localhost/golfgame"

def get_server_link():
  return "http://dounets.com:5003/api/socketApi"
