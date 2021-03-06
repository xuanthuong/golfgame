# -*- coding: utf-8 -*-
# Description: work_history table
# By Thuong.Tran
# Date: 29 Aug 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select, and_
import datetime as dt


class work_history():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _work_history = Table("work_history", _metadata,
                          Column("WRK_HIS_ID", Integer, primary_key=True),
                          Column("USR_ID", Integer),
                          Column("PROC_NM", Text),
                          Column("ST_DT", DateTime),
                          Column("END_DT", DateTime),
                          Column("LD_TM", Float),
                          Column("CRE_DT", DateTime))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.work_history = _work_history
    pass
  
  def insert_to(self, data):
    is_valid = True
    # for item in data:
    #   if not item:
    #     is_valid = False
    #     raise DropItem("Missing %s!" % item)
    if is_valid:
      ins_query = self.work_history.insert().values(data)
      self.connection.execute(ins_query)

  def get_all(self):
    s = select([self.work_history]).order_by('PROC_NM')
    result = self.connection.execute(s)
    return result

  def get_by_period(self, start_date, end_date):
    s = select([self.work_history]).where(and_(self.work_history.c.ST_DT >= start_date, 
                                          self.work_history.c.END_DT <= end_date))
    result = self.connection.execute(s)
    return result
    
  def get_finalized_process_of_one_day(self, today, worker):
    lower = dt.datetime(today.year, today.month, today.day, 0, 0, 0)
    upper = dt.datetime(today.year, today.month, today.day, 23, 59, 59)
    print(lower)
    print(upper)
    s = select([self.work_history]).where(and_(self.work_history.c.END_DT > lower, 
                                              self.work_history.c.END_DT < upper,
                                              self.work_history.c.USR_ID == worker))
    result = self.connection.execute(s)
    return result
    
