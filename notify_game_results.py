# -*- coding: utf-8 -*-
# Description: call procedure
# By Thuong.Tran
# Date: 12 Sept. 2017

from __future__ import division
import datetime as dt
from config import get_DB_URL
from models.sqlprocedure import sqlprocedure


sql_proc = sqlprocedure(get_DB_URL())
class notify_game_results():
  def __init__(self, league_name, start_date, end_date, worker_id):
    self.league_name = league_name
    self.start_date = start_date
    self.end_date = end_date
    self.worker_id = worker_id

  def _get_5_weeks_day(self):
    weeks_list = []
    start_date = self.start_date
    end_date = self.end_date
    for i in range(5):
      weeks_list.append({
        'league_name': self.league_name,
        'start_date': start_date,
        'end_date': end_date,
        'worker_id': self.worker_id
      })
      start_date -= dt.timedelta(days=7)
      end_date -= dt.timedelta(days=7)
    return weeks_list

  def _get_5_weeks_results(self):
    weeks = self._get_5_weeks_day()
    results = []
    if weeks:
      for wk in weeks:
        temp = sql_proc.get_game_results(wk)
        results.append(temp)
      return results

  def _get_5_weeks_avg(self):
    results = self._get_5_weeks_results()
    if results:
      res_data = []
      for i in range(len(results)):
        temp_week = results[i]
        if temp_week:
          temp_week_obj = {}
          cur_week = 'week_' + str(i+1)
          temp_week_obj[cur_week] = {}
          total = 0
          for j in range(len(temp_week)):
            temp_hole = temp_week[j]
            if temp_hole:
              temp_week_obj[cur_week]['hole_' + str(j+1)] = temp_hole['SCRE_NO']
              total += temp_hole['SCRE_NO']
          temp_week_obj[cur_week]['total'] = total
    
          res_data.append(temp_week_obj)
      return res_data

  def _get_game_result_of_current_week(self):
    params = {
      'league_name': self.league_name,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'worker_id': self.worker_id
    }
    game_result = sql_proc.get_game_results(params)
    return game_result


  def call_cal_game_results(self, gm_result):

    table_data = []
    par = {}
    point = {}
    league_avg = {}
    five_week_avg = {}
    temp = {}

    # Game results
    game_result = gm_result._get_game_result_of_current_week()
    for i in range(len(game_result)):
      hole = 'hole_' + str(i+1)
      par[hole] = int(game_result[i]['HOLE_TP'][-1])
      temp[hole] = int(game_result[i]['SCRE_NO'])
      temp_1 = temp[hole] - par[hole]
      if temp_1 >= 0:
        point[hole] = "{0}(+{1})".format(str(temp[hole]), str(temp_1))
      else:
        point[hole] = "{0}({1})".format(str(temp[hole]), str(temp_1))
    par['total'] = sum(par.values())
    point['total'] = sum(temp.values())
    par['hole'] = 'Par'
    point['hole'] = 'Point'

    temp_2 = point['total'] - par['total']
    if temp_2 >= 0:
      point['total'] = "{0}(+{1})".format(str(point['total']), str(temp_2))
    else:
      point['total'] = "{0}({1})".format(str(point['total']), str(temp_2))

    # League average
    lg_avg = sql_proc.get_avg_leage_point(self.league_name)
    for i in range(len(lg_avg[0])):
      hole = 'hole_' + str(i+1)
      league_avg[hole] = round(lg_avg[0][hole], 2)
    league_avg['total'] = sum(league_avg.values())
    league_avg['hole'] = 'League Avg.'

    # 5 weeks average
    results = gm_result._get_5_weeks_avg()
    for j in range(5):
      hole = 'hole_' + str(j+1)
      mytemp = []
      graph_data = []
      for i in range(len(results)):
        week = 'week_' + str(i+1)
        mytemp.append(results[i][week][hole])
        graph_data.append(results[i][week]['total'])
      five_week_avg[hole] = round((sum(mytemp) / len(mytemp)), 2)
    five_week_avg['total'] = sum(five_week_avg.values())
    five_week_avg['hole'] = '5 Weeks Avg.'

    table_data.append(par)
    table_data.append(point)
    table_data.append(league_avg)
    table_data.append(five_week_avg)


    league_avg_graph = []
    for i in range(5):
      league_avg_graph.append(league_avg['total'])

    graph = {
      'labels': ['week 1', 'week 2', 'week 3', 'week 4', 'week 5'],
      'data': [{'name': '5 Weeks Trend', 'data': graph_data}]
    }

    league_list = [{
      'name': self.league_name,
      'date': str(self.start_date) + " ~ " + str(self.end_date),
      'winner': 'Thuong Tran',
      'point': table_data[1]['total'],
      'player': 1
    }]

    temp_graph_data = list(graph_data)
    for i in range(5 - len(temp_graph_data)):
      temp_graph_data.append(0)
    
    response_data = {
      'table': table_data,
      'lineGraph': graph,
      'chartGraph': {
          'labels': ['week 1', 'week 2', 'week 3', 'week 4', 'week 5'],
          'data': [{'name': 'League', 'data': league_avg_graph}, {'name': '5 Weeks', 'data': temp_graph_data}]
      },
      'leagueList': league_list,
      'leagueInfo': {
            'name': self.league_name, 
            'startDate': self.start_date.strftime("%Y-%m-%d"), 
            'end_date': self.end_date.strftime("%Y-%m-%d")
            }
    }


    # print(response_data)
    return response_data


if __name__ == '__main__':
  params = {
      'league_name': '2017 CLT CHAMPION',
      'start_date': dt.date(2017, 9, 11),
      'end_date': dt.date(2017, 9, 15),
      'worker_id': 1
    }
  gm_result = notify_game_results(params['league_name'], params['start_date'], params['end_date'], params['worker_id'])
  print(gm_result.call_cal_game_results(gm_result))