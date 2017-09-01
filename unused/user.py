# -*- coding: utf-8 -*-
# Description: Contains neccessary information of a user
# By Thuong.Tran
# Date: 21 Aug 2017


class user:
  def __init__(self, user_name):
    self.user_name = user_name

  def get_levels(self):
    # get_round_robin(user_name): -> another class
    return [8, 10, 7, 1, 0, 6, 0, 3, 9, 10]