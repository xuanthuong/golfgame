# -*- coding: utf-8 -*-
# Description: league table
# By Thuong.Tran
# Date: 11 Sept. 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, DateTime, Float
from sqlalchemy import select, and_
import datetime as dt


class league():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _league = Table("gmf_leag", _metadata,
                          Column("LEAG_ID", Integer, primary_key=True),
                          Column("LEAG_NM", Text))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.league = _league
    pass

  def insert_to(self, data):
      is_valid = True
      if is_valid:
        ins_query = self.league.insert().values(data)
        self.connection.execute(ins_query)