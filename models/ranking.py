# -*- coding: utf-8 -*-
# Description: ranking table
# By Thuong.Tran
# Date: 11 Sept. 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select, and_
import datetime as dt


class rank():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _rank = Table("gmf_rnk", _metadata,
                          Column("RNK_ID", Integer, primary_key=True),
                          Column("LEAG_NM", Text),
                          Column("RNK_NO", Integer),
                          Column("WRKR_NM", Text),
                          Column("PNT_NO", Integer))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.rank = _rank
    pass

  def insert_to(self, data):
    is_valid = True
    if is_valid:
      ins_query = self.rank.insert().values(data)
      self.connection.execute(ins_query)

  def get_all(self):
    s = select([self.rank]).order_by('RNK_NO')
    result = self.connection.execute(s)
    return result

  def delete_all(self):
    ins_query = self.rank.delete()
    self.connection.execute(ins_query)