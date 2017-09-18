# -*- coding: utf-8 -*-
# Description: call procedure
# By Thuong.Tran
# Date: 12 Sept. 2017

from __future__ import division
import datetime as dt
from config import get_DB_URL
from models.sqlprocedure import sqlprocedure
from models.worker import worker
from models.ranking import rank

DB_URL = get_DB_URL()
sql_proc = sqlprocedure(DB_URL)
day_hole = {'Mon': 'hole_1', 'Tue': 'hole_2', 'Wed': 'hole_3', 'Thu': 'hole_4', 'Fri': 'hole_5'}

class notify_game_results():
  def __init__(self, league_name, start_date, end_date):
    self.league_name = league_name
    self.start_date = start_date
    self.end_date = end_date
    self.week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    self.num_weeks = 5

  def _get_5_weeks_day(self, worker_id):
    weeks_list = []
    start_date = self.start_date
    end_date = self.end_date
    for i in range(self.num_weeks):
      weeks_list.append({
        'league_name': self.league_name,
        'start_date': start_date,
        'end_date': end_date,
        'worker_id': worker_id
      })
      start_date -= dt.timedelta(days=7)
      end_date -= dt.timedelta(days=7)
    return weeks_list

  def _get_5_weeks_results(self, worker_id):
    weeks = self._get_5_weeks_day(worker_id)
    # results = []
    if weeks:
      week_res = {}
      for i in range(len(weeks)):
        wk = 'week_' + str(i+1)
        day_res = {}
        for day in self.week_days:
          day_res[day] = sql_proc.get_all_game_results_by_day(weeks[i], day)
        week_res[wk] = day_res
      return week_res

  def _get_5_weeks_avg(self, worker_id):
    results = self._get_5_weeks_results(worker_id)
    res_data = {}
    week_avg = []
    five_week_trend = []
    if results:
      for day in self.week_days:
        score = 0
        count = 0
        temp = []
        for i in range(len(results)):
          wk = 'week_' + str(i+1)
          sum_score = results[wk][day][0]['SUM_SCRE_NO']
          total_times = results[wk][day][0]['CNT']
          if sum_score:
            score += results[wk][day][0]['SUM_SCRE_NO']
          if total_times:
            count += results[wk][day][0]['CNT']

          if sum_score and total_times:
            temp.append(sum_score / total_times)

        if count > 0:
          res_data[day_hole[day]] = round(score / count, 2)

        week_avg.append(temp)

      for j in range(len(week_avg[0])):
        tmp = 0
        for i in range(len(week_avg)):
          tmp += week_avg[i][j]
        five_week_trend.append(tmp)

    return res_data, five_week_trend

  def _get_best_game_result_by_week(self, worker_id):
    params = {
      'league_name': self.league_name,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'worker_id': worker_id
    }
    game_result = {}
    for day in self.week_days:
      day_result = sql_proc.get_best_game_results_by_day(params, day)
      game_result[day] = day_result[0]
    return game_result


  def call_cal_game_results(self, game_result_obj, worker_id):

    table_data = []
    par = {}
    point = {}
    league_avg = {}
    five_week_avg = {}

    temp_obj = {'Mon': 'hole_1', 'Tue': 'hole_2', 'Wed': 'hole_3', 'Thu': 'hole_4', 'Fri': 'hole_5'}
    # Game results
    game_result = game_result_obj._get_best_game_result_by_week(worker_id)
    temp_point = {}
    for day, value in game_result.items():
      hole = temp_obj[day]
      par[hole] = int(value['HOLE_TP'][-1])
      temp_point[hole] = int(value['SCRE_NO'])

      temp = temp_point[hole] - par[hole]
      if temp >= 0:
        point[hole] = "{0}(+{1})".format(str(temp_point[hole]), str(temp))
      else:
        point[hole] = "{0}({1})".format(str(temp_point[hole]), str(temp))

    par['total'] = sum(par.values())

    point['total'] = sum(temp_point.values())
    temp = point['total'] - par['total']
    if temp >= 0:
      point['total'] = "{0}(+{1})".format(str(point['total']), str(temp))
    else:
      point['total'] = "{0}({1})".format(str(point['total']), str(temp))

    # League average
    lg_avg = sql_proc.get_avg_leage_point(self.league_name)
    for i in range(len(lg_avg[0])):
      hole = 'hole_' + str(i+1)
      league_avg[hole] = round(lg_avg[0][hole], 2)
    league_avg['total'] = round(sum(league_avg.values()), 2)

    # 5 weeks average
    five_week_avg, five_week_trend = game_result_obj._get_5_weeks_avg(worker_id)
    five_week_avg['total'] = round(sum(five_week_avg.values()), 2)
    
    # Column Names
    par['hole'] = 'Par'
    point['hole'] = 'Point'
    league_avg['hole'] = 'League Avg.'
    five_week_avg['hole'] = '5 Weeks Avg.'

    table_data.append(par)
    table_data.append(point)
    table_data.append(league_avg)
    table_data.append(five_week_avg)

    graph = {
      'labels': ['week 1', 'week 2', 'week 3', 'week 4', 'week 5'],
      'data': [{'name': '5 Weeks Trend', 'data': five_week_trend}]
    }

    temp_graph_data = list(five_week_trend)
    for i in range(5 - len(temp_graph_data)):
      temp_graph_data.append(0)

    league_avg_graph = []
    for i in range(len(five_week_trend)):
      league_avg_graph.append(league_avg['total'])
    for i in range(5 - len(five_week_trend)):
      league_avg_graph.append(0)
    
    # Decide winner 
    league_list = [{
      'name': self.league_name,
      'date': str(self.start_date) + " ~ " + str(self.end_date),
      'winner': 'unknow',
      'point': 999,
      'player': 1
    }]

    wk = worker(DB_URL)
    rnk = rank(DB_URL)
    rnk.delete_all()
    temp_ranking = {}
    num_players = 0
    for i in range(1, 3):
      temp_game_results = game_result_obj._get_best_game_result_by_week(i)
      temp_point = {}
      if temp_game_results:
        for day, value in temp_game_results.items():
          hole = temp_obj[day]
          temp_point[hole] = int(value['SCRE_NO'])
        total_points = sum(temp_point.values())

        temp_worker_name = wk.get_username_by_id(i)
        temp_ranking[temp_worker_name] = total_points

        if total_points < league_list[0]['point']:
          league_list[0]['point'] = total_points
          league_list[0]['winner'] = temp_worker_name
        num_players += 1

    league_list[0]['player'] = num_players
    temp_ranking = sorted(temp_ranking.items(), key=lambda x:x[1]) # sort by value of dict

    for i in range(len(temp_ranking)):
      rnk_obj = {
        'LEAG_NM': self.league_name,
        'RNK_NO': i + 1,
        'WRKR_NM': temp_ranking[i][0],
        'PNT_NO': temp_ranking[i][1]
      }
      rnk.insert_to(rnk_obj)

    # Response data
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