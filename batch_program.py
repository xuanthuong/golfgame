# -*- coding: utf-8 -*-
# Description: update workers levels from CFD table
# By Thuong.Tran
# Date: 05 Sept. 2017

import os
from config import get_DB_URL
from models.gmf_cfd import gmf_cfd
from models.work_history import work_history
import datetime as dt
from bson import json_util
import json

DB_URL = get_DB_URL()

cfd_db = gmf_cfd(DB_URL)
whist = work_history(DB_URL)

def get_finalized_process(start_date, today):
  return whist.get_by_period(start_date, today)

def cal_cfd_table(work_his_4_weeks):
  # call api to update
  today = dt.datetime.today()
  start_date = today - dt.timedelta(days=30)
  fn_proc = get_finalized_process(start_date, today)
  proc_list = []
  for p in fn_proc:
    proc_list.append({
      "PROC_NM": p.PROC_NM,
      "ST_DT": p.ST_DT.isoformat(),
      "END_DT": p.END_DT.isoformat(),
      "LD_TM": p.LD_TM
    })
  data = json.dumps({
    "ST_DT": start_date.isoformat(),
    "END_DT": today.isoformat(),
    "processList": proc_list
    })
  headers = {
      "Content-Type": "application/json"
  }
  r = requests.post("https://graph.facebook.com/v2.6/me/messages", headers=headers, data=data)
  if r.status_code != 200:
    print('Status code: ', r.status_code)
    return cfd_result



def get_cfd_table(start_date='2017-07-31 17:00:00', end_date='2017-08-30 17:00:00'):
  return cfd_db.get_by_period(start_date, end_date)

def update_levels(worker):
  finalized_proc = get_finalized_process(today, worker)
  for proc in finalized_proc:
    update(worker, proc)

def update(worker):
  pass



if __name__ == "__main__":
  cal_cfd_table('b')
