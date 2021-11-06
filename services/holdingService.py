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

def updateHolding(email,portfolioId,holdingListObj):
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

def createHolding(email,portfolioId,holdingListObj):
  try:
      user = db.getUserByEmail(email)
      db.getUserPortfolioById(int(portfolioId))
     
      for holdingDict in holdingListObj.holdingList:
        holding = db.UserHolding()
        holding.user = user.subscription_id
        holding.userPortfolio = int(portfolioId)
        holding.stockCode = str(holdingDict['scrip'])
        holding.company = str(holdingDict['company'])
        holding.holdingQuantity = int(holdingDict['quantity'])
        holding.avaragePrice = float(holdingDict['avgPrice'])
        holding.ltp = float(holdingDict['ltp'])
        db.addHolding(holding)

      return {'status' : 200}
        
  except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating user holdings' )



