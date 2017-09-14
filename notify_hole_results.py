# -*- coding: utf-8 -*-
# Description: API server for notify-hole-result
# By Thuong.Tran
# Date: 13 Sept. 2017

from config import get_DB_URL
import datetime as dt
from models.hole_history import hole_history
from models.hole import hole
from models.sqlprocedure import sqlprocedure


def get_hole_results(params):
  DB_URL = get_DB_URL()
  sql_proc = sqlprocedure(DB_URL)
  hole_hist_model = hole_history(DB_URL)
  hole_results = sql_proc.get_hole_results(params)

  response_data = []
  for hole in hole_results:
    hole_data = {
      'HOLE_ID': hole['HOLE_ID'],
      'PLER_ID': hole['PLER_ID'] ,
      'HOLE_TP': hole['HOLE_TP'],
      'HOLE_DT': hole['HOLE_DT'].strftime("%Y-%m-%d"),
      'WK_DY': hole['WK_DY'],
      'GRP_TP': hole['GRP_TP'],
      'WRKR_1_ID': hole['WRKR_1_ID'],
      'WRKR_2_ID': hole['WRKR_2_ID'],
      'SCRE_NO': hole['SCRE_NO']
    }
    # Compute distance
    temp_hole_hist = hole_hist_model.get_by_holeid(hole['HOLE_ID'])
    distance = []
    for temp in temp_hole_hist:
      distance.append(temp['DIST_NO'])

    hole_data['TTL_DIST_NO'] = round(sum(distance),2)

    response_data.append(hole_data)

  return {'data': response_data, 
          'leagueInfo': {
            'name': params['league_name'], 
            'startDate': params['start_date'].strftime("%Y-%m-%d"), 
            'end_date': params['end_date'].strftime("%Y-%m-%d")
            }
          }

def get_hole_details(hole_id):
  DB_URL = get_DB_URL()
  hole_hist_model = hole_history(DB_URL)
  hole_model = hole(DB_URL)
  hole_type = hole_model.get_hole_type_by_id(hole_id)

  hole_hist = []
  temp_hole_hist = hole_hist_model.get_by_holeid(hole_id)
  for hh in temp_hole_hist:
    hole_hist.append({
        'HOLE_ID': hh['HOLE_ID'],
        'CLSS_NO': hh['CLSS_NO'],
        'ORD_NO': hh['ORD_NO'],
        'ACTR_ID': hh['ACTR_ID'],
        'ACT_NM': hh['ACT_NM'],
        'RSLT_NM': hh['RSLT_NM'],
        'ACT_SCRE': hh['ACT_SCRE'],
        'DIST_NO': hh['DIST_NO'],
        'holeType': hole_type['HOLE_TP']
      })
  return {'holeDetail': hole_hist}

# def get_hole_results(params):
#   DB_URL = get_DB_URL()
#   sql_proc = sqlprocedure(DB_URL)
#   hole_hist_model = hole_history(DB_URL)
#   hole_results = sql_proc.get_hole_results(params)

#   response_data = []
#   for hole in hole_results:
#     hole_data = {
#       'HOLE_ID': hole['HOLE_ID'],
#       'PLER_ID': hole['PLER_ID'] ,
#       'HOLE_TP': hole['HOLE_TP'],
#       'HOLE_DT': hole['HOLE_DT'],
#       'WK_DY': hole['WK_DY'],
#       'GRP_TP': hole['GRP_TP'],
#       'WRKR_1_ID': hole['WRKR_1_ID'],
#       'WRKR_2_ID': hole['WRKR_2_ID'],
#       'SCRE_NO': hole['SCRE_NO']
#     }
#     hole_data['TTL_DIST_NO'] = 22222

#     hole_hist = []
#     temp_hole_hist = hole_hist_model.get_by_holeid(hole['HOLE_ID'])
#     for hh in temp_hole_hist:
#       hole_hist.append({
#           'HOLE_ID': hh['HOLE_ID'],
#           'CLSS_NO': hh['CLSS_NO'],
#           'ORD_NO': hh['ORD_NO'],
#           'ACTR_ID': hh['ACTR_ID'],
#           'ACT_NM': hh['ACT_NM'],
#           'RSLT_NM': hh['RSLT_NM'],
#           'ACT_SCRE': hh['ACT_SCRE'],
#           'DIST_NO': hh['DIST_NO'],
#           'holeType': hole['HOLE_TP']
#         })
#     response_data.append({
#       'hole': [hole_data],
#       'holeDetail': hole_hist
#     })
#   return response_data


if __name__ == '__main__':
  params = {
      'league_name': '2017 CLT CHAMPION',
      'start_date': dt.date(2017, 9, 11),
      'end_date': dt.date(2017, 9, 15),
      'worker_id': 1
    }
  print(get_hole_results(params))