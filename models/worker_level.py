# -*- coding: utf-8 -*-
# Description: worker_level_tb table
# By Thuong.Tran
# Date: 29 Aug 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select, update, and_
from sqlalchemy.orm import sessionmaker
import datetime as dt


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
    obj = self.connection.execute(s).fetchone()
    if obj:
      res = [obj['LVL_1_NO'], obj['LVL_2_NO'], obj['LVL_3_NO'], obj['LVL_4_NO'], obj['LVL_5_NO'],
            obj['LVL_6_NO'], obj['LVL_7_NO'], obj['LVL_8_NO'], obj['LVL_9_NO'], obj['LVL_10_NO']]
    # res = [obj.LVL_1_NO, obj.LVL_2_NO, obj.LVL_3_NO, obj.LVL_4_NO, obj.LVL_5_NO,
    #       obj.LVL_6_NO, obj.LVL_7_NO, obj.LVL_8_NO, obj.LVL_9_NO, obj.LVL_10_NO]
    else:
      res = None
    return res

  def get_by_id_and_cfd(self, user_id, cfd_id):
    s = select([self.worker_level_tb]).where(and_(self.worker_level_tb.c.WRKR_ID == user_id,
                                                  self.worker_level_tb.c.CFD_ID == cfd_id))
    obj = self.connection.execute(s).fetchone()
    if obj:
      res = [obj['IDX'], obj['LVL_1_NO'], obj['LVL_2_NO'], obj['LVL_3_NO'], obj['LVL_4_NO'], obj['LVL_5_NO'],
            obj['LVL_6_NO'], obj['LVL_7_NO'], obj['LVL_8_NO'], obj['LVL_9_NO'], obj['LVL_10_NO']]
      # res = [obj.LVL_1_NO, obj.LVL_2_NO, obj.LVL_3_NO, obj.LVL_4_NO, obj.LVL_5_NO,
      #       obj.LVL_6_NO, obj.LVL_7_NO, obj.LVL_8_NO, obj.LVL_9_NO, obj.LVL_10_NO]
      # res = {
      #   'IDX': obj['IDX']
      #   'CFD_ID': obj['LVL_1_NO'],
      #   'WRKR_ID': obj['LVL_1_NO'],
      #   'LVL_1_NO': obj['LVL_1_NO'],
      #   'LVL_2_NO': obj['LVL_1_NO'],
      #   'LVL_3_NO': obj['LVL_1_NO'],
      #   'LVL_4_NO': obj['LVL_1_NO'],
      #   'LVL_5_NO': obj['LVL_1_NO'],
      #   'LVL_6_NO': obj['LVL_1_NO']
      #   'LVL_7_NO': obj['LVL_1_NO'],
      #   'LVL_8_NO': obj['LVL_1_NO'],
      #   'LVL_9_NO': obj['LVL_1_NO'],
      #   'LVL_10_NO': obj['LVL_1_NO']
      # }
    else:
      res = None
    return res

  def merge_to(self, lvl_obj):
    pass

  def update(self, id, obj):
    s = self.worker_level_tb.update().where(self.worker_level_tb.c.IDX == id).values(obj)
    r = self.connection.execute(s)

