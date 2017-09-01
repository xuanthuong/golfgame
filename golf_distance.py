# -*- coding: utf-8 -*-
# Description: Create distance rules for golf game
# By Thuong.Tran
# Date: 28 Aug 2017

import random

class golf_distance:
  def __init__(self, hole):
    self.hole = hole

    self.avg_dist_par3 = 229
    self.avg_dist_par4 = 430
    self.avg_dist_par5 = 527

    self.avg_dist_driving = 191.5
    self.avg_dist_putt = 3.0
    self.avg_dist_2nd_shot = self.avg_dist_par3 - self.avg_dist_driving - self.avg_dist_putt
    self.avg_dist_3rd_shot = self.avg_dist_par4 - self.avg_dist_driving - self.avg_dist_putt - self.avg_dist_2nd_shot
    self.avg_dist_4th_shot = self.avg_dist_par5 - self.avg_dist_driving - self.avg_dist_putt - self.avg_dist_2nd_shot - self.avg_dist_3rd_shot

    self.delta_dist_driving = 30.0
    self.delta_dist_2nd_shot = 10.0
    self.delta_dist_3rd_shot = 10.0
    self.delta_dist_4th_shot = 10.0
    self.delta_dist_putt = 1.5

  def get_actual_driving_dist(self):
    rnd = random.uniform(-1, 1)
    return self.avg_dist_driving + rnd * self.delta_dist_driving
  
  def get_actual_2nd_shot(self):
    rnd = random.uniform(-1, 1)
    return self.avg_dist_2nd_shot + rnd * self.delta_dist_2nd_shot

  def get_actual_3rd_shot(self):
    rnd = random.uniform(-1, 1)
    return self.avg_dist_3rd_shot + rnd * self.delta_dist_3rd_shot

  def get_actual_4th_shot(self):
    rnd = random.uniform(-1, 1)
    return self.avg_dist_4th_shot + rnd * self.delta_dist_4th_shot

  def get_actual_putting(self):
    rnd = random.uniform(-1, 1)
    return self.avg_dist_putt + rnd * self.delta_dist_putt

  def get_distance(self, action, next_action):
    distance = 0
    if self.hole == 'Par3':
      distance = self.get_par3_dist(action, next_action)
    elif self.hole == 'Par4':
      distance = self.get_par4_dist(action, next_action)
    elif self.hole == 'Par5':
      distance = self.get_par5_dist(action, next_action)
    return distance
  
  def get_par3_dist(self, action, next_action):
    if action == 'driving_shot' and next_action != 'inhole':
      return self.get_actual_driving_dist()
    elif action == 'driving_shot' and next_action == 'inhole':
      return self.avg_dist_par3
    elif action == 'approach' and next_action == 'putting':
      return self.get_actual_2nd_shot()
    elif action == 'approach' and next_action == 'inhole':
      return self.avg_dist_putt + self.avg_dist_2nd_shot
    elif action == 'approach' and next_action != 'inhole' and next_action != 'putting':
      return 0
    elif action == 'putting' and next_action == 'inhole':
      return self.get_actual_putting()
    else:
      return 0

  def get_par4_dist(self, action, next_action):
    if action == 'driving_shot' and next_action == 'second_shot':
      return self.get_actual_driving_dist()
    elif action == 'driving_shot' and next_action == 'approach':
      return self.get_actual_driving_dist() + self.get_actual_2nd_shot()
    elif action == 'driving_shot' and next_action == 'inhole':
      return self.avg_dist_par4
    elif action == 'driving_shot' and next_action != 'inhole' and next_action != 'second_shot' and next_action != 'approach':
      return 0
    
    elif action == 'second_shot' and next_action == 'approach':
      return self.get_actual_2nd_shot()
    elif action == 'second_shot' and next_action == 'putting':
      return self.get_actual_2nd_shot() + self.get_actual_3rd_shot()
    elif action == 'second_shot' and next_action == 'inhole':
      return self.get_actual_2nd_shot() + self.get_actual_3rd_shot() + self.get_actual_putting()
    elif action == 'second_shot' and next_action != 'approach' and next_action != 'putting' and next_action != 'inhole':
      return 0
    
    elif action == 'approach' and next_action == 'putting':
      return self.get_actual_3rd_shot()
    elif action == 'approach' and next_action == 'inhole':
      return self.get_actual_3rd_shot() + self.get_actual_putting()
    elif action == 'approach' and next_action != 'putting' and next_action != 'inhole':
      return 0

    elif action == 'putting' and next_action == 'inhole':
      return self.get_actual_putting()
    elif action == 'putting' and next_action != 'inhole':
      return 0

    else: 
      return 0

  def get_par5_dist(self, action, next_action):
    if action == 'driving_shot' and next_action == 'second_shot':
      return self.get_actual_driving_dist()
    elif action == 'driving_shot' and next_action == 'third_shot':
      return self.get_actual_driving_dist() + self.get_actual_2nd_shot()
    elif action == 'driving_shot' and next_action == 'approach':
      return self.get_actual_driving_dist() + self.get_actual_2nd_shot() + self.get_actual_3rd_shot()
    elif action == 'driving_shot' and next_action != 'second_shot' and next_action != 'third_shot' and next_action != 'approach':
      return 0
    
    elif action == 'second_shot' and next_action == 'third_shot':
      return self.get_actual_2nd_shot()
    elif action == 'second_shot' and next_action == 'approach':
      return self.get_actual_2nd_shot() + self.get_actual_3rd_shot()
    elif action == 'second_shot' and next_action == 'putting':
      return self.get_actual_2nd_shot() + self.get_actual_3rd_shot() + self.get_actual_4th_shot()
    elif action == 'second_shot' and next_action == 'inhole':
      return self.get_actual_2nd_shot() + self.get_actual_3rd_shot() + self.get_actual_4th_shot() + self.get_actual_putting()
    elif action == 'second_shot' and (next_action == 'bunker' or next_action == 'water' or next_action == 'ruff'):
      return 0

    elif action == 'third_shot' and next_action == 'approach':
      return self.get_actual_3rd_shot()
    elif action == 'third_shot' and next_action == 'putting':
      return self.get_actual_3rd_shot() + self.get_actual_4th_shot()
    elif action == 'third_shot' and next_action == 'inhole':
      return self.get_actual_3rd_shot() + self.get_actual_4th_shot() + self.get_actual_putting()
    elif action == 'third_shot' and (next_action == 'bunker' or next_action == 'water' or next_action == 'ruff'):
      return 0
    
    elif action == 'approach' and next_action == 'putting':
      return self.get_actual_4th_shot()
    elif action == 'approach' and next_action == 'inhole':
      return self.get_actual_4th_shot() + self.get_actual_putting()

    elif action == 'approach' and (next_action == 'bunker' or next_action == 'water' or next_action == 'ruff'):
      return 0
    
    elif action == 'putting' and next_action == 'inhole':
      return self.get_actual_putting()
    
    else:
      return 0