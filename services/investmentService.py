# investmentService.py
import traceback
import database.stock_holding_db as db
from exception.apiError import APIError

def getInvestment(email,portfolioId):
    try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      investmentList = db.getInvestmentByUserAndUserPortfolio(user.subscription_id,user_portfolio.id)
      return {'investmentList' : investmentList}
    except Exception:
      raise APIError(statusCode = 400, message = 'error occured while loading user investments' )
