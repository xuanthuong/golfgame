# -*- coding: utf-8 -*-
# Description: worker_level_tb table
# By Thuong.Tran
# Date: 29 Aug 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


class worker_level():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _worker_level_tb = Table("gmf_wrkr_lvl", _metadata,
                          Column("IDX", Integer, primary_key=True),
                          Column("CFD_ID", Integer),
                          Column("WRKR_ID", Integer),
                          Column("LVL_1_NO", Integer),
                          Column("LVL_2_NO", Integer),
                          Column("LVL_3_NO", Integer),
                          Column("LVL_4_NO", Integer),
                          Column("LVL_5_NO", Integer),
                          Column("LVL_6_NO", Integer),
                          Column("LVL_7_NO", Integer),
                          Column("LVL_8_NO", Integer),
                          Column("LVL_9_NO", Integer),
                          Column("LVL_10_NO", Integer))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.worker_level_tb = _worker_level_tb
    pass
  
  def insert_to(self, data):
    is_valid = True
    if is_valid:
      ins_query = self.worker_level_tb.insert().values(data)
      self.connection.execute(ins_query)

  def get_all(self):
    s = select([self.worker_level_tb])
    result = self.connection.execute(s)
    return result
  
  def get_by_id(self, user_id):
    s = select([self.worker_level_tb]).where(self.worker_level_tb.c.WRKR_ID == user_id)
    r = self.connection.execute(s)
    for obj in r:
      return [obj['LVL_1_NO'], obj['LVL_2_NO'], obj['LVL_3_NO'], obj['LVL_4_NO'], obj['LVL_5_NO'],
              obj['LVL_6_NO'], obj['LVL_7_NO'], obj['LVL_8_NO'], obj['LVL_9_NO'], obj['LVL_10_NO']]