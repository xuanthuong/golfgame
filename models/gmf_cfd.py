# -*- coding: utf-8 -*-
# Description: cfd table
# By Thuong.Tran
# Date: 05 Sept 2017

# Reference: http://pythoncentral.io/sqlalchemy-orm-examples/
#            http://www.mysqltutorial.org/stored-procedures-parameters.aspx
#            http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters

import os
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy import select, and_
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class gmf_cfd(Base):
  __tablename__ = 'gmf_cumlt_freq_distr'

  id = Column(Integer, primary_key=True)
  CFD_ID = Column(Integer)
  PROC_TP_NM = Column(String)
  SEQ_NO = Column(Integer)
  CFD_NM = Column(String)
  LOWR_BND_NO = Column(Float)
  UPPR_BND_NO = Column(Float)
  FREQ_NO = Column(Integer)
  CUMLT_NO = Column(Integer)
  PCT_NO = Column(Float)
  LVL_NO = Column(Integer)
  ST_DT = Column(DateTime)
  END_DT = Column(DateTime)
  createdAt = Column(DateTime, default=func.now())
  updatedAt = Column(DateTime, default=func.now())

  def __init__(self, DB_URL):
    _engine = create_engine(DB_URL)
    _session = sessionmaker()
    _session.configure(bind=_engine)
    Base.metadata.create_all(_engine)
    self.session = _session()

  def get_all(self):
    return self.session.query(gmf_cfd)

  def get_by_period(self, start_date, end_date):
    return self.session.query(gmf_cfd).filter(and_(
      gmf_cfd.ST_DT == start_date,
      gmf_cfd.END_DT == end_date))

  def get_level(self, proc_name, leadtime, start_date, end_date):    
    query = select([gmf_cfd.CFD_ID, gmf_cfd.LVL_NO]).where(and_(
      gmf_cfd.PROC_TP_NM == proc_name,
      gmf_cfd.LOWR_BND_NO < leadtime,
      gmf_cfd.UPPR_BND_NO > leadtime,
      gmf_cfd.ST_DT == start_date,
      gmf_cfd.END_DT == end_date))

    # query = self.session.query(gmf_cfd).filter(and_(
    #   gmf_cfd.PROC_TP_NM == proc_name,
    #   gmf_cfd.LOWR_BND_NO < leadtime,
    #   gmf_cfd.UPPR_BND_NO > leadtime,
    #   gmf_cfd.ST_DT == start_date,
    #   gmf_cfd.END_DT == end_date))

    return self.session.execute(query).fetchone()
    

  def sp_test_1(self, test_id):
    query = 'call test_procedure(%d)'%test_id
    # try:
    result = self.session.execute(query).fetchall()
    return result
    # except exc.DBAPIError, e: #Proper way of reconnecting?
    #   t.rollback()
    #   time.sleep(5)
    #   self._connection = self._engine.connect()
    #   Session = sessionmaker(bind=self._engine)
    #   self._session = Session()
    # except:
    #   t.rollback()
    # return None
    
  def exec_procedure(session, proc_name, params):
    pass
    # https://stackoverflow.com/questions/3563738/stored-procedures-with-sqlalchemy