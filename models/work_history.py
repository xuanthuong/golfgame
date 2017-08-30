# -*- coding: utf-8 -*-
# Description: work_history table
# By Thuong.Tran
# Date: 29 Aug 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select


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
    s = select([self.work_history])
    result = self.connection.execute(s)
    return result
