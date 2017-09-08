# -*- coding: utf-8 -*-
# Description: update workers levels from CFD table
# By Thuong.Tran
# Date: 05 Sept. 2017

import os
from config import get_DB_URL
from models.gmf_cfd import gmf_cfd
from models.work_history import work_history
from models.worker_level import worker_level
from play_new_game import play_game
import datetime as dt
from bson import json_util
import json
import time
import random as rd
import requests


DB_URL = get_DB_URL()

cfd_db = gmf_cfd(DB_URL)
wkhist = work_history(DB_URL)
wk_level = worker_level(DB_URL)

START_DATE ='2017-07-31 17:00:00'
END_DATE ='2017-08-30 17:00:00'

def get_finalized_process():
  return wkhist.get_by_period(START_DATE, END_DATE)

def cal_cfd_table():
  # call api to update
  fn_proc = get_finalized_process(START_DATE, END_DATE)

  proc_list = []
  for p in fn_proc:
    proc_list.append({
      "PROC_NM": p.PROC_NM,
      "ST_DT": p.ST_DT.isoformat(),
      "END_DT": p.END_DT.isoformat(),
      "LD_TM": p.LD_TM
    })
  data = json.dumps({
    "ST_DT": START_DATE.isoformat(),
    "END_DT": END_DATE.isoformat(),
    "processList": proc_list
    })
  headers = {
      "Content-Type": "application/json"
  }
  r = requests.post("https://xxx.com", headers=headers, data=data)
  if r.status_code != 200:
    print('Status code: ', r.status_code)
    return cfd_result

def get_level_obj(new_lvl, cfd_id, worker, levels):
  return {
        'CFD_ID': cfd_id,
        'WRKR_ID': worker,
        'LVL_1_NO': new_lvl,
        'LVL_2_NO': levels[1],
        'LVL_3_NO': levels[2],
        'LVL_4_NO': levels[3],
        'LVL_5_NO': levels[4],
        'LVL_6_NO': levels[5],
        'LVL_7_NO': levels[6],
        'LVL_8_NO': levels[7],
        'LVL_9_NO': levels[8],
        'LVL_10_NO': levels[9]
        }

def update_levels(today, worker):
  finalized_proc = wkhist.get_finalized_process_of_one_day(today, worker)# today -> each day 8pm
  for proc in finalized_proc:
    print('finalized process: ', proc)
    r = cfd_db.get_level(proc.PROC_NM, proc.LD_TM, START_DATE, END_DATE)
    # Xu ly khi lead time cua process user moi hoan thanh ko nam trong range cua cfd_table
    # Lam sao de biet duoc cfd_id khi ma cfd_table ko co gia tri do
    print('got level: ', r)
    new_lvl = r['LVL_NO']
    cfd_id = r['CFD_ID']
    print('cfd_id: %s' % cfd_id)
    print('new level: %s' % new_lvl)
    print('worker id: %s' % worker)

    levels = wk_level.get_by_id_and_cfd(worker, cfd_id)
    if levels:
      wk_level.update(levels[0], get_level_obj(new_lvl, cfd_id, worker, levels))
    else:
      wk_level.insert_to(get_level_obj(new_lvl, cfd_id, worker, levels))

def pause():
  print("Press any key to continue ...")
  input()


def decide_winner(week):
  pass


if __name__ == "__main__":
  # END_DATE = dt.datetime.today()
  # START_DATE = today - dt.timedelta(days=30)
  # cal_cfd_table('b')

  # time.sleep(5) # for updating cfd data

  week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
  hole_types = {'Mon': "Par3", "Tue": "Par4", "Wed": "Par3", "Thu": "Par5", "Fri": "Par5"}
  proc_list = ['A']
  workers_list = [1, 2, 3, 4]
  num_tasks = 2
  max_lt = 8

  # day = 'Mon'

  for day in week_days:  
    print("[%s] - System start batch job" % day)
    pause()
    print("[%s] - System get finialized processes of all user" % day)
    for wk_id in workers_list:
      for i in range(rd.randint(1, num_tasks)):
        today = dt.datetime.today()
        lead_time = round(rd.uniform(1.0, max_lt), 2)
        start_time = today - dt.timedelta(days=lead_time)
        data = {'USR_ID': wk_id,
                'PROC_NM': rd.choice(proc_list),
                'ST_DT': start_time,
                'END_DT': today,
                'LD_TM': lead_time,
                'CRE_DT': today}
        wkhist.insert_to(data)

    time.sleep(5)
    # pause()

    print("[%s]- System update work level for all user" % day)
    for wk_id in workers_list:
      today = dt.datetime.today()
      update_levels(today, wk_id)

    # pause()
    print("[%s] - System is playing game for all user" % day)

    for user_id in workers_list:
      hole = hole_types[day]
      user_name = 'ThuongTran'

      if user_name != "All":
        game = play_game(hole, user_name, user_id)
        game_data = game.start_game()
        game_data = json.dumps(game_data)
        if game_data:
          print("Hole Result: ")
          print(game_data)
        else:
          print("No game data")
      else:
        print("No username")

      # NOTIFY TO SOCKET IO
      print("[%s] - system notify result to users" % day)
      headers = {
          "Content-Type": "application/json"
      }
      # r = requests.post("https://gamification-pm.herokuapp.com/api/socketApi", headers=headers, data=game_data)
      r = requests.post("http://dounets.com:5003/api/socketApi", headers=headers, data=game_data)
      
      if r.status_code == 200:
        print('Done game result notification - Status code: ', r.status_code)

      print("[%s] - Finish notify to user %s" % (day, user_id))
      pause()


  print("[Sun] - batch job are updating cfd table")

  print("Repeat.....next week ......")