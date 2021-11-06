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
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/stock_holding_db_local?charset=utf8mb4",pool_size=10,max_overflow=20)
elif env.mysql_instance == 'vm':
    engine = create_engine("mysql+pymysql://app:rajwaitu@localhost:3306/stock_holding_db?charset=utf8mb4",pool_size=10,max_overflow=20)

#engine = create_engine("mysql+pymysql://root:root@localhost:3306/stock_holding_db?charset=utf8mb4",pool_size=10,max_overflow=20)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plan'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    #users = relationship("User", back_populates="subscription",uselist=False) 

class PortfolioClass(Base):
    __tablename__ = 'portfolio_class'

    code = Column(String, primary_key=True)
    name = Column(String)

class User(Base):
    __tablename__ = 'users'

    subscription_id = Column(String, primary_key=True)
    user_name = Column(String)
    email = Column(String)
    user_password = Column(String)
    subscription_plan = Column(Integer, ForeignKey('subscription_plan.id'))
    activation_date = Column(DateTime, default=datetime.datetime.utcnow)
    expiry_date = Column(DateTime, default=datetime.datetime.utcnow)
    subscription = relationship("SubscriptionPlan",uselist=False)

class UserPortfolio(Base):
    __tablename__ = 'user_portfolio'

    id = Column(Integer, primary_key=True)
    portfolioName = Column('portfolio',String)
    user = Column('subscription_id',String, ForeignKey('users.subscription_id'))
    portfolioClass = Column('portfolio_code',String, ForeignKey('portfolio_class.code'))
    portfolioType = relationship("PortfolioClass")

class UserHolding(Base):
    __tablename__ = 'holding'

    id = Column(Integer, primary_key=True)
    company = Column('company_name',String)
    stockCode = Column('symbol',String)
    holdingQuantity = Column('quantity',Integer)
    avaragePrice = Column('avarage_price',Float)
    user = Column('subscription_id',String, ForeignKey('users.subscription_id'))
    userPortfolio = Column('portfolio',Integer, ForeignKey('user_portfolio.id'))
    ltp = Column(Float)
    maxima = Column(Float)
    depth = Column(Float)

class UserInvestment(Base):
    __tablename__ = 'investment'

    id = Column(Integer, primary_key=True)
    holdingDate = Column('holding_date',Date)
    investmentAmount = Column('investment_amount',Integer)
    holdingValue = Column('holding',Integer)
    profitLoss = Column('profit_loss',Integer)
    user = Column('subscription_id',Integer, ForeignKey('users.subscription_id'))
    userPortfolio = Column('portfolio',Integer, ForeignKey('user_portfolio.id'))

class UserWatchlist(Base):
    __tablename__ = 'user_watchlist'

    id = Column(Integer, primary_key=True)
    companyCode = Column('company_code',String)
    watchlistPrice = Column('watchlist_price',Float)
    created = Column('created',Date)
    user = Column('user',Integer, ForeignKey('users.subscription_id'))

#query begins

def getSubscriptionPlan():
    subscriptionList = []
    subscriptions_query = select(SubscriptionPlan)
    connection = engine.connect()
    ResultProxy = connection.execute(subscriptions_query)
    ResultSet = ResultProxy.fetchall()
    for x in ResultSet:
        subscriptionList.append(x.name)

    print(type(ResultSet))
    return {'subscriptions' : subscriptionList }

def getUsers():
    userList = []
    user_query = select(User)
    connection = engine.connect()
    ResultProxy = connection.execute(user_query)
    ResultSet = ResultProxy.fetchall()
    for x in ResultSet:
        print((type(x.subscription_plan)))
        userList.append(x.user_name)

    return {'users' : userList }

def getUserByEmail(email):
    session = Session()
    try:
      user = session.query(User).filter(User.email == email).one()
    except MultipleResultsFound:
       raise APIError(statusCode = 400, message = 'multiple user record found for given email' )
    except NoResultFound:
       raise APIError(statusCode = 400, message = 'no user record found for given email' )
    return user

def getUserPortfolioById(id):
    session = Session()
    user_portfolio = session.query(UserPortfolio).filter(UserPortfolio.id == id).one()
    if user_portfolio == None:
        raise APIError(statusCode = 400, message = 'no portfolio found for given id' )
    return user_portfolio

def getUserPortfolioByUser(user_subscription_id):
    session = Session()
    user_portfolio_list = session.query(UserPortfolio).filter(UserPortfolio.user == user_subscription_id)
    return user_portfolio_list


def getHoldingByUserAndUserPortfolio(user_subscription_id,portfolio_id):
    session = Session()
    user_holding_list = session.query(UserHolding).filter(UserHolding.user == user_subscription_id,UserHolding.userPortfolio == portfolio_id).all()
    return user_holding_list;

def getInvestmentByUserAndUserPortfolio(user_subscription_id,portfolio_id):
    session = Session()
    user_investment_list = session.query(UserInvestment).filter(UserInvestment.user == user_subscription_id,UserInvestment.userPortfolio == portfolio_id).all()
    return user_investment_list;

def createInvestment(userInvestment):
    session = Session()
    try:
     session.add(userInvestment)
     session.commit()
    finally:
     session.close()

def addHolding(userHolding):
    session = Session()
    try:
     session.add(userHolding)
     session.commit()
    finally:
     session.close()

def updateHoldingLTP(ltpDict):
    session = Session()
    try:
        session.query(UserHolding).filter(UserHolding.id.in_(ltpDict)).update({
        UserHolding.ltp: case(ltpDict,value=UserHolding.id)}, synchronize_session=False)
        session.commit()
    except Exception:
        print(traceback.format_exc())
        session.rollback()
    finally:
     session.close()

def updateHoldingMaxima(maximaDict):
    session = Session()
    try:
        session.query(UserHolding).filter(UserHolding.id.in_(maximaDict)).update({
        UserHolding.maxima: case(maximaDict,value=UserHolding.id)}, synchronize_session=False)
        session.commit()
    except Exception:
        print(traceback.format_exc())
        session.rollback()
    finally:
     session.close()

def updateHoldingDepth(depthDict):
    session = Session()
    try:
        session.query(UserHolding).filter(UserHolding.id.in_(depthDict)).update({
        UserHolding.depth: case(depthDict,value=UserHolding.id)}, synchronize_session=False)
        session.commit()
    except Exception:
        print(traceback.format_exc())
        session.rollback()
    finally:
     session.close()


def getUserWatchList(user_subscription_id):
    session = Session()
    user_watchlist = session.query(UserWatchlist).filter(UserWatchlist.user == user_subscription_id).all()
    return user_watchlist;

def addUsers():
    user = User()
    subscription = SubscriptionPlan()
    subscription.id = 1
    subscription.name = 'Free'
    ins = insert(User).values(subscription_id='abc',user_name='jack', email='abc@test.com',
    user_password='abc',activation_date=None,expiry_date=None,subscription_plan=1)
    
    connection = engine.connect()
    connection.execute(ins)

    return {'result' : 'user added' }
