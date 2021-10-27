from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from sqlalchemy.sql import select,insert,case
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import datetime
from sqlalchemy.sql.sqltypes import Date, Float

from exception.apiError import APIError
import traceback
import config.app_env as env

if env.mysql_instance == 'local':
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/stocks_db?charset=utf8mb4",pool_size=10,max_overflow=20)
elif env.mysql_instance == 'vm':
    engine = create_engine("mysql+pymysql://app:rajwaitu@localhost:3306/stocks_db?charset=utf8mb4",pool_size=10,max_overflow=20)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Stocks(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    scrip = Column(String)
    sector = Column(String)
    trend_12_mm = Column(Integer)
    trend_6_mm = Column(Integer)
    price_change = Column(Float)
    active = Column(Integer)

#query begins

def getStocksByTrend(period,trend):
    session = Session()
    if period == 12:
        stock_list = session.query(Stocks).filter(Stocks.trend_12_mm == trend,Stocks.active == 1).all()
    elif period == 6:
        stock_list = session.query(Stocks).filter(Stocks.trend_6_mm == trend,Stocks.active == 1).all()

    return stock_list;

