# -*- coding: utf-8 -*-
# Description: Configure enviroment vairables
# By Thuong.Tran
# Date: 21 Aug 2017

import os

def get_DB_URL():
  return os.environ['GOLF_GAME_DB_URL']
