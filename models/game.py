# -*- coding: utf-8 -*-
# Description: game table
# By Thuong.Tran
# Date: 11 Sept. 2017

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, Date, Float
from sqlalchemy import select, and_
import datetime as dt


class game():
  def __init__(self, db_url):
    _engine = create_engine(db_url)
    _connection = _engine.connect()
    _metadata = MetaData()
    _game = Table("gmf_game", _metadata,
                  Column("GAME_ID", Integer, primary_key=True),
                  Column("GAME_NM", Text),
                  Column("GAME_TP", Text),
                  Column("ST_DT", Date),
                  Column("END_DT", Date),
                  Column("LEAG_ID", Integer),
                  Column("PLY_TP", Text),
                  Column("WINR_TP", Text),
                  Column("CFD_ID", Integer))
    _metadata.create_all(_engine)
    self.connection = _connection
    self.game = _game
    pass

  def insert_to(self, data):
      is_valid = True
      if is_valid:
        ins_query = self.game.insert().values(data)
        self.connection.execute(ins_query)