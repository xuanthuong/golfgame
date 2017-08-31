# -*- coding: utf-8 -*-
# Description: gmf_hole table
# By Thuong.Tran
# Date: 31 Aug 2017


from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select


class hole():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _gmf_hole = Table("gmf_hole", _metadata,
                          Column("HOLE_ID", Integer, primary_key=True),
                          Column("PLER_ID", Integer),
                          Column("HOLE_TP", Text),
                          Column("HOLE_DT", DateTime),
                          Column("WK_DY", Text),
                          Column("GRP_TP", Text),
                          Column("WRKR_1_ID", Integer),
                          Column("WRKR_2_ID", Integer),
                          Column("SCRE_NO", Float))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.gmf_hole = _gmf_hole
    pass
  
  def insert_to(self, data):
    is_valid = True
    if is_valid:
      ins_query = self.gmf_hole.insert().values(data)
      r = self.connection.execute(ins_query)
      return r.lastrowid


  def get_all(self):
    s = select([self.gmf_hole]).order_by('HOLE_ID')
    result = self.connection.execute(s)
    return result
