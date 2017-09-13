# -*- coding: utf-8 -*-
# Description: player table
# By Thuong.Tran
# Date: 11 Sept. 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, Date, Float
from sqlalchemy import select, and_
import datetime as dt


class player():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _player = Table("gmf_player", _metadata,
                  Column("PLER_ID", Integer, primary_key=True),
                  Column("GAME_ID", Integer),
                  Column("PLER_TP", Text),
                  Column("SCRE_NO", Integer),
                  Column("GRD_NO", Integer),
                  Column("TEAM_ID", Integer))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.player = _player
    pass

  def insert_to(self, data):
      is_valid = True
      if is_valid:
        ins_query = self.player.insert().values(data)
        self.connection.execute(ins_query)