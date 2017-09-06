# -*- coding: utf-8 -*-
# Description: update workers levels from CFD table
# By Thuong.Tran
# Date: 05 Sept. 2017

import os
from config import get_DB_URL
from models.gmf_cfd import gmf_cfd
from models.work_history import work_history
import datetime as dt

DB_URL = get_DB_URL()

cfd_db = gmf_cfd(DB_URL)
whist = work_history(DB_URL)

def get_finalized_process(today=dt.datetime.today()):
  start_date = today - dt.timedelta(days=30)
  print('start date: %s' % start_date)
  print('end date: %s' % today)
  return whist.get_by_period(start_date, today)

def get_cfd_table(start_date='2017-07-31 17:00:00', end_date='2017-08-30 17:00:00'):
  return cfd_db.get_by_period(start_date, end_date)

def update_levels(worker):
  finalized_proc = get_finalized_process(today, worker)
  for proc in finalized_proc:
    update(worker, proc)

def update(worker):
  pass

def cal_cfd_table(work_his_4_weeks):
  # call api to update
  pass

# for proc in get_cfd_table():
#   print(proc.PROC_TP_NM)

result = get_finalized_process()
i = 0
for pro in result:
  print(pro)
  i += 1
print(i)
