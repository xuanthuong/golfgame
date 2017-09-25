# -*- coding: utf-8 -*-
# Description: player_group table
# By Thuong.Tran
# Date: 11 Sept. 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, Date, Float
from sqlalchemy import select, and_
import datetime as dt


class player_group():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _player_group = Table("gmf_player_group", _metadata,
                  Column("GAME_ID", Integer, primary_key=True),
                  Column("GAME_ID", Integer),
                  Column("PLER_ID", Integer),
                  Column("WRKR_ID", Integer),
                  Column("PLER_GRP_NM", Text),
                  Column("GRP_CLSS_TP", Text))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.player_group = _player_group
    pass

  def insert_to(self, data):
      is_valid = True
      if is_valid:
        ins_query = self.player_group.insert().values(data)
        r = self.connection.execute(ins_query)
        return r.lastrowid