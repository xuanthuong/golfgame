# -*- coding: utf-8 -*-
# Description: hole_history table
# By Thuong.Tran
# Date: 31 Aug 2017


from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select


class hole_history():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _hole_history = Table("gmf_hole_his", _metadata,
                          Column("IDX", Integer, primary_key=True),
                          Column("HOLE_ID", Integer),                          
                          Column("CLSS_NO", Integer),
                          Column("ORD_NO", Integer),
                          Column("ACTR_ID", Integer),
                          Column("ACT_NM", Text),
                          Column("RSLT_NM", Text),
                          Column("ACT_SCRE", Float),
                          Column("DIST_NO", Float))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.hole_history = _hole_history
    pass
  
  def insert_to(self, data):
    is_valid = True
    # for item in data:
    #   if not item:
    #     is_valid = False
    #     raise DropItem("Missing %s!" % item)
    if is_valid:
      ins_query = self.hole_history.insert().values(data)
      r = self.connection.execute(ins_query)


  def get_all(self):
    s = select([self.hole_history]).order_by('HOLE_ID')
    result = self.connection.execute(s)
    return result
