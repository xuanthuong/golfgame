# -*- coding: utf-8 -*-
# Description: Generate example input data for gamification
# By Thuong.Tran
# Date: 21 Aug 2017

import datetime as dt
import random as rd
from models.work_history import work_history

DB_URL = "mysql://golf_user:dounets123!@localhost/golfgame"

def gen_rand_work_history(start, end):
  wrk_hist = work_history(DB_URL)
  result = wrk_hist.get_all()
  records = []

  print("Retrieved data from database")
  for r in result:
    records.append({
    'USR_ID': r['USR_ID'],
    'PROC_NM': r['PROC_NM'],
    'ST_DT': r['ST_DT'],
    'END_DT': r['END_DT'],
    'LD_TM': r['LD_TM'],
    'CRE_DT': r['CRE_DT']
    })
  
  if len(records) > 0:
    return records
  records = []
  
  today = dt.datetime.today()
  for i in range(30):
    user_id = rd.randint(1,2)
    process_type = rd.choice(['A', 'B'])
    start_time = gen_rand_datetime(start, end)
    lead_time = round(rd.uniform(1.0, 10.0), 2)
    end_time = start_time + dt.timedelta(days=lead_time)
    records.append({
      'USR_ID': user_id,
      'PROC_NM': process_type,
      'ST_DT': start_time,
      'END_DT':end_time,
      'LD_TM': lead_time,
      'CRE_DT': today
    })

  print("Created new work history data")
  for rec in records:
    wrk_hist.insert_to(rec)
  return records


def gen_rand_datetime(start, end):
  from_day = start[0]
  from_month = start[1]
  from_year = start[2]

  to_day = end[0]
  to_month = end[1]
  to_year = end[2]

  year = rd.randint(from_year, to_year)
  month = rd.randint(from_month, to_month)
  # max_day_of_month = get_max_day_of_month(month)
  max_day_of_month = 31
  day = rd.randint(1, max_day_of_month)
  hour = rd.randint(0, 23)
  minutue = rd.randint(1, 59)
  second = rd.randint(1, 59)
  rnd_date = dt.datetime(year, month, day, hour, minutue, second)

  return rnd_date


def convert_to_d_h_m_s(days):
  """Return the tuple of days, hours, minutes and seconds from days (float)"""

  days, fraction = divmod(days, 1)
  hours, fraction = divmod(fraction * 24, 1)
  minutes, fraction = divmod(fraction * 60, 1)
  seconds = fraction * 60
  
  return int(days), int(hours), int(minutes), int(seconds)


# print(convert_to_d_h_m_s(0.56))
# format_dt = rnd_date.strftime("%d-%m-%Y %H:%M")

# def convert_to_d_h_m_s(seconds):
#     """Return the tuple of days, hours, minutes and seconds from seconds"""

#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     days, hours = divmod(hours, 24)

#     return days, hours, minutes, seconds