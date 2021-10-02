# holdingService.py
import traceback
import database.stock_holding_db as db
from exception.apiError import APIError

def getHolding(email,portfolioId):
    try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      holdingList = db.getHoldingByUserAndUserPortfolio(user.subscription_id,user_portfolio.id)
      return {'holdingList' : holdingList}
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while loading user holdings' )


