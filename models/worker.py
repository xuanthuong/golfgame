# -*- coding: utf-8 -*-
# Description: worker_tb table
# By Thuong.Tran
# Date: 29 Aug 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select


class worker():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _worker_tb = Table("gmf_wrkr", _metadata,
                          Column("WRKR_ID", Integer, primary_key=True),
                          Column("WRKR_NM", Text),
                          Column("CRE_DT", DateTime))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.worker_tb = _worker_tb
    pass
  
  def insert_to(self, data):
    is_valid = True
    if is_valid:
      ins_query = self.worker_tb.insert().values(data)
      self.connection.execute(ins_query)

  def get_all(self):
    s = select([self.worker_tb])
    result = self.connection.execute(s)
    return result

  def get_by_username(self, user_name):
    s = select([self.worker_tb]).where(self.worker_tb.c.WRKR_NM == user_name.lower())
    r = self.connection.execute(s)
    for obj in r:
      return obj['WRKR_ID']

  def get_username_by_id(self, user_id):
    s = select([self.worker_tb]).where(self.worker_tb.c.WRKR_ID == user_id)
    r = self.connection.execute(s)
    for obj in r:
      return obj['WRKR_NM']
  