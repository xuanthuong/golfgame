# -*- coding: utf-8 -*-
# Description: call procedure
# By Thuong.Tran
# Date: 12 Sept. 2017

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class sqlprocedure():
  
  def __init__(self, DB_URL):
    _engine = create_engine(DB_URL)
    _session = sessionmaker()
    _session.configure(bind=_engine)
    self.session = _session()

  def exec_procedure(self, proc_name, params):
    sql_params = ",".join(["@{0}={1}".format(name, value) for name, value in params.items()])
    sql_string = "call {proc_name}({params})".format(proc_name=proc_name, params=sql_params)
    print(sql_string)
    return self.session.execute(sql_string).fetchall()

  def call_procedure(self, query):
    result = self.session.execute(query).fetchall()
    return result

  def get_best_game_results_by_day(self, params, day):
    query = "call get_best_game_results_by_day({0}, '{1}', '{2}', '{3}', '{4}')" \
            .format(params['worker_id'], params['league_name'], 
                    params['start_date'], params['end_date'], day)
    return self.call_procedure(query)

  def get_all_game_results_by_day(self, params, day):
    query = "call get_all_game_results_by_day({0}, '{1}', '{2}', '{3}', '{4}')" \
            .format(params['worker_id'], params['league_name'], 
                    params['start_date'], params['end_date'], day)
    return self.call_procedure(query)

  def get_avg_leage_point(self, league_name):
    query = "call get_average_league_point('{0}')".format(league_name)
    return self.call_procedure(query)

  def get_hole_results(self, params):
    query = "call get_hole_results({0}, '{1}', '{2}', '{3}')" \
            .format(params['worker_id'], params['league_name'], 
                    params['start_date'], params['end_date'])
    return self.call_procedure(query)

