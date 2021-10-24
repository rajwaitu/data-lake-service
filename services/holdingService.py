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

def createOrUpdateHolding(email,portfolioId,holdingListObj):
  try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      ltpDict = {}
      maximaDict = {}
      depthDict = {}

      for holdingDict in holdingListObj.holdingList:
        id = int(holdingDict['id'])
        ltpDict[id] = float(holdingDict['ltp'])
        maximaDict[id] = float(holdingDict['maxima'])
        depthDict[id] = float(holdingDict['depth'])

      db.updateHoldingLTP(ltpDict)
      db.updateHoldingMaxima(maximaDict)
      db.updateHoldingDepth(depthDict)
        
  except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating/updating user holdings' )



